import asyncio
from playwright.async_api import async_playwright
EX='/home/claude/test/node_modules/three/examples/js/'
CO="!document.getElementById('custom').classList.contains('hide')"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-gl=swiftshader','--disable-dev-shm-usage','--js-flags=--max-old-space-size=4096'])
        ctx=await b.new_context(viewport={'width':480,'height':270})
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
        await H.evaluate("(()=>{PH='net1';enterNet('net1');})()"); await H.wait_for_timeout(3000)
        await until(G,"__t.MODE==='play'",30,'guest play')
        await H.evaluate("__t.V.inv=1e9;__t.M.inv=1e9")
        await G.evaluate("styleSet('blade')"); await G.wait_for_timeout(2500)
        q="JSON.stringify({arm:ARM,V:(__t.V.bladeG||[]).map(s=>s.visible),M:(__t.M.bladeG||[]).map(s=>s.visible),myw:typeof MYW!=='undefined'?MYW:null})"
        print('H after guest blade',await H.evaluate(q),flush=True)
        print('G after guest blade',await G.evaluate(q),flush=True)
        await H.evaluate("(()=>{const z=__t.ZONES[0];__t.V.x=z.x;__t.V.z=z.z;startEncounter(z,false);})()")
        await until(H,"cusOpenH()",20,'h open'); await until(G,"cusOpenH()",20,'g open')
        print('open h/g',await H.evaluate(CO),await G.evaluate(CO),flush=True)
        await G.evaluate("closeCustom()"); await G.wait_for_timeout(1000)
        await H.evaluate("closeCustom()"); await H.wait_for_timeout(2500)
        print('after close h/g',await H.evaluate(CO),await G.evaluate(CO),'frozen',await H.evaluate("worldFrozen()"),'gfz',await G.evaluate("__t.NET.fz"),'paused',await H.evaluate("paused"),await G.evaluate("paused"),'cwait',await H.evaluate("document.getElementById('cwait').className"),await G.evaluate("document.getElementById('cwait').className"),flush=True)
        await H.evaluate("styleSet('blade')"); await H.wait_for_timeout(2000)
        print('H after host blade',await H.evaluate(q),flush=True)
        print('G after host blade',await G.evaluate(q),flush=True)
        print('roles',await H.evaluate("[NET.host,NET.guest]"),await G.evaluate("[NET.host,NET.guest]"),'PH',await H.evaluate("__t.PH"),flush=True)
        print('errs',errs,flush=True); await b.close()
asyncio.run(main())
