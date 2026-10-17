import bpy,sys,os,time
src=open('/mnt/user-data/uploads/Downloads/nl_kk/nl_hyrig_v2.py',encoding='utf-8').read()
lm=open('/tmp/claude-0/bl/autolm.py',encoding='utf-8').read()
lm=lm.replace("crotch=min(max(crotch or .42,.36),.5)","crotch=float(os.environ['CROTCH']) if os.environ.get('CROTCH') else min(max(crotch or .42,.36),.5)")
lm=lm.replace("for z in range(int(.2*N),int(.78*N)):","for z in range(int(.2*N),int(float(os.environ.get('ARMTOP','.78'))*N)):")
fix=lambda t:t.replace("bpy.context.window.scene=sc","(setattr(bpy.context.window,'scene',sc) if bpy.context.window else None)").replace("bpy.context.window.scene=bpy.data.scenes['NL_AR']","pass")
src=src.replace("    r=min(1.0,tris/len(M.data.polygons))","    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=float(os.environ.get('WELD','0.0005')));bpy.ops.object.mode_set(mode='OBJECT');print('welded',len(M.data.vertices),flush=True)\n    r=min(1.0,tris/len(M.data.polygons))")
exec(fix(lm));exec(fix(src))
D='/mnt/user-data/uploads/Downloads/nl_kk/'
OUT='/tmp/claude-0/rig/out/'
k=sys.argv[1];fn=os.environ.get('SRC') or '/mnt/user-data/uploads/Downloads/tp_%s.glb'%k
V=load_V(fn);LM,meta,img=auto_lm(V)
if os.environ.get('TPOSE'):
    N=img.shape[0]-1;H=meta['H'];s_=H/N;tci=meta['tci']
    band=[]
    for z in range(int(.6*N),int(.95*N)):
        rs=runs(img[z]);c=[r for r in rs if r[0]<=tci<=r[1]]
        if c and (c[0][1]-c[0][0])*s_>.5*H:band.append((z,c[0]))
    zs=[z for z,_ in band];az=(sum(zs)/len(zs))/N*H
    ext=max(max(r[1]-tci,tci-r[0]) for _,r in band)*s_
    cr=float(os.environ.get('CROTCH','.47'));nk=float(os.environ.get('NECK','0'))*H or LM['neck']
    shx=LM['sh'][0];sh_z=az+.005*H
    LM['sh']=(shx,0,sh_z);LM['el']=(shx+(ext-shx)*.47,0,sh_z);LM['ha']=(shx+(ext-shx)*.86,0,sh_z);LM['tip']=(ext,0,sh_z)
    hpz=cr*H;LM['hp']=(LM['hp'][0],0,hpz);LM['hips']=(hpz+.04*H,0.0);LM['neck']=nk;LM['head']=nk+.05*H
    LM['spine']=LM['hips'][0]+(nk-LM['hips'][0])*.25;LM['chest']=LM['hips'][0]+(nk-LM['hips'][0])*.5;LM['uchest']=LM['hips'][0]+(nk-LM['hips'][0])*.75
    LM['kn']=(LM['kn'][0],0,float(os.environ.get('KNEE','.27'))*H)
    print('BAND',len(band),round(az,3),round(ext,3))
print('META',{a:(b if not isinstance(b,list) else len(b)) for a,b in meta.items()})
print('LM',{a:(tuple(round(x,3) for x in b) if isinstance(b,tuple) else round(b,3)) for a,b in LM.items()},flush=True)
overlay(img,LM,meta,'/tmp/claude-0/look/lm_%s.png'%k)
if os.environ.get('DRY'):sys.exit(0)
r=hyrig('tp_'+k,fn,LM,tris=int(os.environ.get('TRIS','24000')),tex=1024)
os.replace(r['out'],OUT+'hy_%s.glb'%k);print('done',r['size'])
