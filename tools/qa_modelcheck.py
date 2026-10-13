# 自動モデルチェック（公開前に毎回実行）
#  1) 関節の曲がる向き：走り/待機アニメでひざ＝前、ひじ＝後ろに曲がっているかを数値判定
#  2) 専用カメラで4方向×(待機/走り)＋頭アップを撮影 → sheet.png（顔の両面・逆関節・破綻を目視確認）
#  3) 後頭部の「顔らしさ」チェック：頭の前後アップの類似度が高すぎたら警告
import asyncio,sys,json,base64,io
import numpy as np
from PIL import Image,ImageDraw
from playwright.async_api import async_playwright
EX='/home/claude/test/node_modules/three/examples/js/'
OUT='/tmp/claude-0/qa/'
CHARS="{leo:__t.LEO,molly:__t.MOLLY,volt:CH3D.V,mist:CH3D.M,dad:typeof DAD!=='undefined'?DAD:null,bro1:typeof BRO1!=='undefined'?BRO1:null}"
JS_SETUP=r"""(()=>{if(window.__QAI)return 1;const qa={};qa.cam=new THREE.PerspectiveCamera(35,1,.05,100);qa.cam.layers.enableAll();qa.rt=new THREE.WebGLRenderTarget(320,320);
 qa.hemi=new THREE.HemisphereLight('#ffffff','#556070',1.0);qa.dir=new THREE.DirectionalLight('#ffffff',1.1);
 qa.grp=new THREE.Group();qa.grp.position.set(6000,0,6000);scene.add(qa.grp);qa.grp.add(qa.hemi);qa.dir.position.set(6003,6,6004);qa.dir.target.position.set(6000,0,6000);scene.add(qa.dir,qa.dir.target);
 const fl=new THREE.Mesh(new THREE.CircleGeometry(3,40),new THREE.MeshStandardMaterial({color:'#9aa0a8'}));fl.rotation.x=-Math.PI/2;fl.position.y=.001;qa.grp.add(fl);
 window.__QAI=qa;return 1;})()"""
JS_SHOT=r"""((k,pose,yaw,dist,ty,t)=>{const qa=window.__QAI;const C=%s;const c=C[k];if(!c||!c.g)return null;
 const keep={x:c.x,z:c.z,y:c.y,face:c.face,rotY:c.rotY,vis:c.g.visible,par:c.g.parent,sc:c.g.scale.x,ry:c.g.rotation.y};
 if(!c.g.parent)scene.add(c.g);c.g.visible=true;c.g.scale.setScalar(1);c.g.position.set(6000,0,6000);c.g.rotation.y=0;
 const clip=pose==='run'?'Jog_Fwd_Loop':'Idle_Loop';const a=c.acts&&c.acts[clip];if(a){c.mixer.stopAllAction();a.reset();a.play();a.setEffectiveWeight(1);c.mixer.update(a.getClip().duration*t);if(c.tb)retarget(c);}
 c.g.updateMatrixWorld(true);
 let hy=1.5;if(c.tb&&c.tb.Head){hy=c.tb.Head.getWorldPosition(new THREE.Vector3()).y;}
 const tyy=ty<0?hy+.05:ty;const cx=6000+Math.sin(yaw)*dist,cz=6000+Math.cos(yaw)*dist;qa.cam.position.set(cx,tyy+(ty<0?0:.15),cz);qa.cam.lookAt(6000,tyy,6000);qa.cam.updateMatrixWorld(true);
 const prevBg=scene.background,prevFog=scene.fog;scene.background=new THREE.Color('#d8dde4');scene.fog=null;
 renderer.setRenderTarget(qa.rt);renderer.clear();renderer.render(scene,qa.cam);const px=new Uint8Array(320*320*4);renderer.readRenderTargetPixels(qa.rt,0,0,320,320,px);renderer.setRenderTarget(null);
 scene.background=prevBg;scene.fog=prevFog;
 c.mixer.stopAllAction();c.cur=null;c.x=keep.x;c.z=keep.z;c.face=keep.face;c.rotY=keep.rotY;c.g.visible=keep.vis;c.g.scale.setScalar(keep.sc);if(!keep.par)scene.remove(c.g);c.g.position.set(keep.x,keep.y||0,keep.z);c.g.rotation.y=keep.ry;
 let s='';for(let i=0;i<px.length;i+=8192)s+=String.fromCharCode.apply(null,px.subarray(i,i+8192));return btoa(s);})""" % CHARS
JS_JOINTS=r"""(()=>{const R={};const W=b=>b.getWorldPosition(new THREE.Vector3());const C=%s;
 for(const [k,c] of Object.entries(C)){if(!c||!c.tb||!c.acts){R[k]='nochar';continue;}
  const keep={face:c.face,rotY:c.rotY,ry:c.g.rotation.y};c.g.rotation.y=0;const out={};
  for(const cl of ['Jog_Fwd_Loop','Sprint_Loop','Idle_Loop']){const a=c.acts[cl];if(!a)continue;c.mixer.stopAllAction();a.reset();a.play();a.setEffectiveWeight(1);
   const kn=[],el=[];
   for(let i=0;i<24;i++){c.mixer.update(i?(a.getClip().duration/24):0);retarget(c);c.g.updateMatrixWorld(true);const f=new THREE.Vector3(0,0,1).applyQuaternion(c.g.getWorldQuaternion(new THREE.Quaternion()));
    ['L','R'].forEach(S=>{const H=W(c.tb[S+'_UpperLeg']),K=W(c.tb[S+'_LowerLeg']),A=W(c.tb[S+'_Foot']);const d=K.clone().sub(H.clone().add(A).multiplyScalar(.5));d.y=0;
     if(K.clone().sub(H).angleTo(A.clone().sub(K))*57.3>12)kn.push(d.dot(f));
     const Sh=W(c.tb[S+'_UpperArm']),E=W(c.tb[S+'_LowerArm']),Hd=W(c.tb[S+'_Hand']);const d2=E.clone().sub(Sh.clone().add(Hd).multiplyScalar(.5));d2.y=0;
     if(E.clone().sub(Sh).angleTo(Hd.clone().sub(E))*57.3>15)el.push(d2.dot(f));});}
   out[cl]={kneeFwd:kn.length?+(kn.filter(v=>v>0).length/kn.length).toFixed(2):null,elbowBack:el.length?+(el.filter(v=>v<0).length/el.length).toFixed(2):null};}
  c.mixer.stopAllAction();c.cur=null;c.face=keep.face;c.rotY=keep.rotY;c.g.rotation.y=keep.ry;R[k]=out;}
 return JSON.stringify(R);})()""" % CHARS
def img(b64):
    a=np.frombuffer(base64.b64decode(b64),dtype=np.uint8).reshape(320,320,4)[::-1,:,:3];return Image.fromarray(a.copy())
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader']); pg=await b.new_page(viewport={'width':640,'height':360})
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('**/build/three.min.js',lambda r:r.fulfill(path='/tmp/claude-0/three.min.js'))
        async def ex(route):
            f=route.request.url.split('/examples/js/')[1]; await route.fulfill(path=EX+f,content_type='application/javascript')
        await pg.route('**/examples/js/**',ex)
        await pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        await pg.goto('http://localhost:8778/index.html'); await pg.wait_for_timeout(2500)
        await pg.evaluate("window.__autoDlg=true;window.__autoChoice=1;window.__noSAO=true;try{localStorage.clear()}catch(e){}"); await pg.click("#start")
        E_=pg.evaluate
        for i in range(200):
            if await E_("__t.PH==='rooms0'&&!__t.busy&&!__t.DLGS"): break
            await pg.wait_for_timeout(1000)
        await pg.wait_for_timeout(1500)
        J=json.loads(await E_(JS_JOINTS)); await E_(JS_SETUP)
        ks=[k for k in ['leo','molly','volt','mist','dad','bro1'] if J.get(k)!='nochar']
        views=[('front',0),('back',3.14159),('left',1.5708),('right',-1.5708)]
        S=200;cols=[f'{p}_{v}' for p in ['idle','run'] for v,_ in views]+['headF','headB']
        sheet=Image.new('RGB',(S*len(cols),S*len(ks)),'#222');report=[]
        for r,k in enumerate(ks):
            shots={}
            for pose,t in [('idle',.3),('run',.25)]:
                for v,yw in views:
                    shots[f'{pose}_{v}']=img(await E_(f"{JS_SHOT}('{k}','{pose}',{yw},3.2,.9,{t})"))
            for v,yw in [('headF',0),('headB',3.14159)]:
                shots[v]=img(await E_(f"{JS_SHOT}('{k}','idle',{yw},.95,-1,.3)"))
            for c,n in enumerate(cols):sheet.paste(shots[n].resize((S,S)),(c*S,r*S))
            d=ImageDraw.Draw(sheet);d.text((4,r*S+4),k,fill='red')
            f=np.asarray(shots['headF'].convert('L'),float);bk=np.asarray(shots['headB'].convert('L').transpose(Image.FLIP_LEFT_RIGHT),float)
            cc=np.corrcoef(f.ravel(),bk.ravel())[0,1]
            jr=J.get(k,{});bad=[]
            for cl,v in (jr.items() if isinstance(jr,dict) else []):
                if v['kneeFwd'] is not None and v['kneeFwd']<.8:bad.append(f'{cl}:ひざ逆({v["kneeFwd"]})')
                if cl!='Idle_Loop' and v['elbowBack'] is not None and v['elbowBack']<.5:bad.append(f'{cl}:ひじ逆({v["elbowBack"]})')
            if cc>.85:bad.append(f'後頭部が顔と酷似({cc:.2f})')
            report.append((k,'OK' if not bad else 'NG',bad,round(cc,2)))
        sheet.save(OUT+'sheet.png')
        for r in report:print('CHECK',*r)
        print('errs',errs[:5]); await b.close()
asyncio.run(main())
