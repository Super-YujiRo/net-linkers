import asyncio
from playwright.async_api import async_playwright
EX='/home/claude/test/node_modules/three/examples/js/'
CO="!document.getElementById('custom').classList.contains('hide')"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--disable-dev-shm-usage','--js-flags=--max-old-space-size=4096'])
        ctx=await b.new_context(viewport={'width':480,'height':270})
        await ctx.add_init_script("try{localStorage.setItem('nl_qual','3')}catch(e){}")
        errs={'h':[],'g':[]}
        async def setup(pg,tag):
            pg.on('pageerror',lambda e:errs[tag].append(str(e)))
            pg.on('console',lambda m: errs[tag].append(m.text) if m.type=='error' and 'Failed to load' not in m.text else None)
            await pg.route('**/build/three.min.js',lambda r:r.fulfill(path='/tmp/claude-0/three.min.js'))
            async def ex(route):
                f=route.request.url.split('/examples/js/')[1]; await route.fulfill(path=EX+f,content_type='application/javascript')
            await pg.route('**/examples/js/**',ex)
            await pg.route('**/fonts.googleapis.com/**',lambda r:r.abort())
        H=await ctx.new_page(); await setup(H,'h'); G=await ctx.new_page(); await setup(G,'g')
        await H.goto('http://localhost:8778/index.html?bc=1'); await H.wait_for_timeout(2000)
        await H.click('#p2'); await H.click('#onl'); await H.wait_for_timeout(500); await H.click('#rmol')
        for i in range(30):
            await H.wait_for_timeout(500)
            if await H.evaluate("!!document.getElementById('invite')"): break
        url=await H.evaluate("document.getElementById('invite').value"); code=await H.evaluate("document.getElementById('roomCode').textContent")
        print('url',url,flush=True)
        print('code',code,flush=True)
        await G.goto(url); await G.wait_for_timeout(3000); await G.click("#gjoin")
        C,J=H,G
        H,G=J,C
        async def until(pg,expr,sec=120,label=''):
            for i in range(sec):
                try:
                    if await pg.evaluate(expr): return True
                except Exception as e: pass
                await pg.wait_for_timeout(1000)
            print('TIMEOUT',label or expr,flush=True); return False
        await until(H,"!!document.getElementById('hstart')&&!document.getElementById('hstart').classList.contains('hide')",300,'hstart')
        await H.evaluate("window.__autoDlg=true"); await H.evaluate("document.getElementById('hstart').click()")
        await until(H,"__t.PH==='rooms0'&&!__t.DLGS",200,'rooms0')
        await until(G,"__t.MODE==='room'&&!__t.DLGS",60,'guest room')
        await H.evaluate("window.__autoDlg=true"); await G.evaluate("window.__autoDlg=true")
        log=[]
        def P(*x):
            print(*x,flush=True);log.append(x)
        GS="JSON.stringify([__t.MODE,typeof SCN!=='undefined'?SCN:null,typeof ROOM_OF!=='undefined'?ROOM_OF.molly:null,!!__t.DLGS,typeof wOf==='function'&&__t.M?wOf(__t.M):null,__t.PH])"
        HS="JSON.stringify([MODE,SCN,ROOM_OF.leo,ROOM_OF.molly,busyStory,REQ_ON,zenny,!!DLGS,!!CHOICE,typeof wOf==='function'?[wOf(V),wOf(M)]:null])"
        async def run(js,label,sec=90):
            await H.evaluate("window.__s=0;(async()=>{try{"+js+";window.__s=1}catch(e){window.__s='ERR '+e.message}})();0")
            for i in range(sec):
                v=await H.evaluate("window.__s")
                if v: break
                await H.wait_for_timeout(1000)
            P(label,'->',v,'H',await H.evaluate(HS),'G',await G.evaluate(GS))
        async def clearZone(zexpr,label):
            for i in range(120):
                st=await H.evaluate(f"(()=>{{const z={zexpr};if(!z)return 'nozone';if(!z.act&&!z.clear&&MODE==='play'&&!busyStory)startEncounter(z,false);if(z.act)for(const e of liveEn())hurtEnemy(e,99999,{{x:V.x,z:V.z}},{{ignoreShield:1}});if(typeof closeCustom==='function'&&!$('custom').classList.contains('hide'))closeCustom();if(!$('bust').classList.contains('hide'))closeBust();if(!$('result').classList.contains('hide'))$('rbtn').click();return JSON.stringify([z.act,z.clear,MODE,busyStory])}})()")
                await G.evaluate("(()=>{try{if(typeof closeCustom==='function'&&!$('custom').classList.contains('hide'))closeCustom();if(!$('result').classList.contains('hide'))$('rbtn').click();}catch(e){}})();0")
                if '"room",false' in st: break
                await H.wait_for_timeout(1000)
            P(label,st,'H',await H.evaluate(HS),'G',await G.evaluate(GS))
        await H.evaluate("FL.nc1=1;FL.nc1done=1;FL.nc1River=1;window.__autoChoice=0;window.__autoDlg=true;0");await G.evaluate("window.__autoChoice=0;window.__autoDlg=true;0")
        # 1) レオ側のおつかい（餃子屋）
        await run("await reqTalk('gyoza','sys')","gyoza talk+dive")
        P('guest during dive',await G.evaluate(GS))
        await clearZone("REQZ['gyoza']","gyoza clear")
        # 2) モリー専用（さくら）をゲスト操作として
        await run("NET.actor='molly';INTER_ACTOR=__t.MOLLY;try{await reqTalk('sakura','molly')}finally{NET.actor=null;INTER_ACTOR=null}","sakura talk+dive")
        await clearZone("REQZ['sakura']","sakura clear")
        await run("await reqTalk('dad','dad')","dad talk+dive");await clearZone("REQZ['dad']","dad clear")
        await run("await reqTalk('angler','sys')","angler talk+dive");await clearZone("REQZ['angler']","angler clear")
        P('reqAll',await H.evaluate("[FL.reqAll,reqCount&&reqCount(),zenny]"))
        # 3) 第2章
        await run("await ch2Start()","ch2Start")
        await H.evaluate("C2CUE.splice(0,C2CUE.length,['ウキが、ふわっと浮きあがった！',1]);0")
        await run("ACT='leo';await ch2Fish(0)","fish leo")
        await run("NET.actor='molly';INTER_ACTOR=__t.MOLLY;try{await ch2Fish(1)}finally{NET.actor=null;INTER_ACTOR=null}","fish molly(guest)")
        for i in range(60):
            if await H.evaluate("FL.ch2out&&!busyStory"): break
            await H.wait_for_timeout(1000)
        P('blackout',await H.evaluate("JSON.stringify([FL.ch2out,ROOMS.maisaka.lamps.map(l=>l.pool.visible)])"),'Glamps',await G.evaluate("JSON.stringify(ROOMS.maisaka.lamps.map(l=>l.pool.visible))"))
        await run("ACT='leo';await ch2Ice()","ice leo")
        await H.evaluate("window.__autoChoice=2;0")
        await run("NET.actor='molly';INTER_ACTOR=__t.MOLLY;try{await ch2Radio()}finally{NET.actor=null;INTER_ACTOR=null}","radio molly(guest)")
        await H.evaluate("window.__autoChoice=0;0")
        P('tasks',await H.evaluate("JSON.stringify([FL.c2ice,FL.c2radio,FL.c2pads,PADS.length])"))
        await run("await ch2Dive()","ch2Dive")
        P('guest in net?',await G.evaluate(GS))
        await clearZone("ZONES.find(z=>z.navi==='wavem')","wave boss")
        for i in range(90):
            if await H.evaluate("FL.ch2done&&!busyStory&&MODE==='room'"): break
            await H.evaluate("if(!$('bust').classList.contains('hide'))closeBust();if(!$('result').classList.contains('hide'))$('rbtn').click();0")
            await G.evaluate("(()=>{try{if(!$('result').classList.contains('hide'))$('rbtn').click();}catch(e){}})();0")
            await H.wait_for_timeout(1000)
        P('end H',await H.evaluate("JSON.stringify([FL.ch2done,PH,MODE,ROOM_OF.leo,ROOM_OF.molly,PACK.map(c=>c[0]).includes('wavek')])"),'G',await G.evaluate(GS))
        await G.screenshot(path='/tmp/claude-0/qa/onq_guest.png',timeout=180000)
        print('errs',{k:v[:6] for k,v in errs.items()},flush=True); await b.close()
asyncio.run(main())
