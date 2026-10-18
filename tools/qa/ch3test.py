import asyncio,json
from playwright.async_api import async_playwright
EX='/home/claude/test/node_modules/three/examples/js/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--disable-dev-shm-usage','--js-flags=--max-old-space-size=4096']);pg=await b.new_page(viewport={'width':640,'height':360})
        errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.add_init_script("try{localStorage.setItem('nl_qual','3')}catch(e){}")
        await pg.route('**/build/three.min.js',lambda r:r.fulfill(path='/tmp/claude-0/three.min.js'))
        async def ex(route):
            f=route.request.url.split('/examples/js/')[1];await route.fulfill(path=EX+f,content_type='application/javascript')
        await pg.route('**/examples/js/**',ex);await pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        print('launched',flush=True)
        await pg.goto('http://localhost:8778/index.html');await pg.wait_for_timeout(2500)
        await pg.evaluate("window.__autoDlg=true;window.__autoChoice=0;window.__noSAO=true;try{localStorage.clear()}catch(e){}");await pg.click('#start')
        E=pg.evaluate
        for i in range(200):
            if await E("typeof __t!=='undefined'&&__t.PH==='rooms0'&&!__t.busy"):break
            await pg.wait_for_timeout(1000)
        await pg.wait_for_timeout(1500)
        log=[]
        async def until(js,n=120,dt=500):
            for i in range(n):
                v=await E(js)
                if v:return v
                await pg.wait_for_timeout(dt)
            return None
        await E("FL.nc1=1;FL.nc1done=1;REQ_IDS.forEach(id=>{FL['rq_'+id]=1;FL['rqd_'+id]=1});FL.reqAll=1;FL.ch2=1;FL.ch2done=1;PH='c2free';window.__s=0;talkPC('leo').then(()=>window.__s=1);0")
        log.append(('morning',await until("window.__s===1"),await E("JSON.stringify([PH,FL.ch3,townOpen('shinhama'),objBase])")));print(log[-1],flush=True)
        await E("window.__s=0;(async()=>{await goRoom(__t.LEO,'shinhama',22,2.4,-Math.PI/2);await ch3Arrive(__t.LEO);window.__s=1;})();0")
        log.append(('arrive',await until("window.__s===1"),await E("JSON.stringify([ROOM_OF.leo,ROOM_OF.molly,FL.c3arr])")));print(log[-1],flush=True)
        await pg.screenshot(path='/tmp/claude-0/qa/c3arr.png',timeout=180000)
        await E("window.__autoChoice=0;ACT='leo';window.__s=0;ch3Office().then(()=>window.__s=1);0");await until("window.__s===1")
        log.append(('officeWrong',await E("FL.c3office||0")))
        await E("window.__autoChoice=1;window.__s=0;ch3Office().then(()=>window.__s=1);0");await until("window.__s===1")
        await E("window.__autoChoice=0;ACT='molly';window.__s=0;ch3Board().then(()=>window.__s=1);0");await until("window.__s===1")
        log.append(('tasks',await E("JSON.stringify([FL.c3office,FL.c3board,FL.c3pads,PADS.length])")));print(log[-1],flush=True)
        await E("ACT='leo';window.__s=0;ch3Dive().then(()=>window.__s=1);0");await until("window.__s===1")
        log.append(('net',await E("JSON.stringify([MODE,SCN,wOf(V),PH])")));print(log[-1],flush=True)
        await E("V.x=IAREAS.erail.o[0];V.z=IAREAS.erail.o[1]+36;0")
        log.append(('crow',await until("FL.c3crow&&!busyStory",60),await E("FL.c3crow")));print(log[-1],flush=True)
        z="ZONES.find(z=>z.navi==='linerm')";shots=0;await E("window.__shots=0")
        for i in range(200):
            st=await E(f"(()=>{{const z={z};return JSON.stringify([z.act,z.clear,liveEn().length,paused,busyStory,!!DLGS,FL.ch3done||0,MODE])}})()")
            if '"room"' in st and ',1,' in st:break
            await E(f"(()=>{{const z={z};if(!$('custom').classList.contains('hide'))closeCustom();if(!$('bust').classList.contains('hide'))closeBust();if(!z.act&&!z.clear&&MODE==='play'&&!busyStory){{window.__zu=[z.hx,z.hz,z.x,z.z,V.x,V.z];startEncounter(z,false);}}if(z.act&&window.__shots>=4)for(const e of liveEn())hurtEnemy(e,99999,{{x:V.x,z:V.z}},{{ignoreShield:1}});if(!$('result').classList.contains('hide'))$('rbtn').click();}})()")
            J=json.loads(st)
            if J[0] and shots<4 and J[2]>0 and J[7]=='play':
                await pg.wait_for_timeout(1200);await pg.screenshot(path=f'/tmp/claude-0/qa/lboss{shots}.png',timeout=180000);shots+=1;await E(f"window.__shots={shots}")
                if shots==1:print('zu',await E("JSON.stringify(window.__zu)"),flush=True)
            await pg.wait_for_timeout(500)
        log.append(('boss',st));print(log[-1],flush=True)
        log.append(('end',await E("JSON.stringify([FL.ch3done,PH,MODE,ROOM_OF.leo,ROOMS.shinhama.trains[0].visible,PACK.map(c=>c[0]).includes('linerk'),objBase])")))
        await pg.screenshot(path='/tmp/claude-0/qa/ch3end.png',timeout=180000)
        for l in log:print(l,flush=True)
        print('errs',errs[:5]);await b.close()
asyncio.run(main())
