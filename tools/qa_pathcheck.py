import asyncio,json
from playwright.async_api import async_playwright
EX='/home/claude/test/node_modules/three/examples/js/'
JS=r"""(()=>{const key='factory',R=ROOMS[key];const M=.2;const hit=(x,z)=>{const lx=x-R.ox,lz=z-R.oz;return BLOCK.some(b=>b.room===key&&lx>b.x0-M&&lx<b.x1+M&&lz>b.z0-M&&lz<b.z1+M);};
 const cases=[[[-5.4,4.4],[-3.4,3.4]],[[-4.3,4.4],[-2.5,3.55]],[[1,-.6],[-1.7,1.45]],[[-3.4,3.4],[-6.9,-3.1]],[[-2.5,3.55],[-6.9,-4.1]]];const out=[{w:R.w,d:R.d,blocks:BLOCK.filter(b=>b.room===key).map(b=>[b.x0,b.z0,b.x1,b.z1].map(v=>+v.toFixed(2)))}];
 for(const [a,b] of cases){const sx=R.ox+a[0],sz=R.oz+a[1];const p=autoPath(sx,sz,R.ox+b[0],R.oz+b[1],key);let bad=0,cx=sx,cz=sz;
  // simulate straight vs path
  let sbad=0;for(let t=0;t<=60;t++){const x=sx+(R.ox+b[0]-sx)*t/60,z=sz+(R.oz+b[1]-sz)*t/60;if(hit(x,z))sbad++;}
  if(p)for(const w of p){const n=Math.ceil(Math.hypot(w[0]-cx,w[1]-cz)/.05);for(let t=1;t<=n;t++){if(hit(cx+(w[0]-cx)*t/n,cz+(w[1]-cz)*t/n))bad++;}cx=w[0];cz=w[1];}
  out.push({sHit:hit(sx,sz),gHit:hit(R.ox+b[0],R.oz+b[1]),a,b,straightHits:sbad,pathPts:p?p.length:null,pathHits:bad});}
 return JSON.stringify(out);})()"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--disable-dev-shm-usage']);pg=await b.new_page(viewport={'width':640,'height':360})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('**/build/three.min.js',lambda r:r.fulfill(path='/tmp/claude-0/three.min.js'))
        async def ex(route):
            f=route.request.url.split('/examples/js/')[1];await route.fulfill(path=EX+f,content_type='application/javascript')
        await pg.route('**/examples/js/**',ex);await pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        await pg.goto('http://localhost:8778/index.html');await pg.wait_for_timeout(2500)
        await pg.evaluate("window.__autoDlg=true;window.__autoChoice=1;window.__noSAO=true;try{localStorage.clear()}catch(e){}");await pg.click("#start")
        for i in range(200):
            if await pg.evaluate("typeof __t!=='undefined'&&__t.PH==='rooms0'&&!__t.busy"):break
            await pg.wait_for_timeout(1000)
        await pg.wait_for_timeout(1500)
        for r in json.loads(await pg.evaluate(JS)):print(r)
        print('errs',errs[:3]);await b.close()
asyncio.run(main())
