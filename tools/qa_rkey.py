import asyncio,json
from playwright.async_api import async_playwright
EX='/home/claude/test/node_modules/three/examples/js/'
JS=r"""(()=>{const a=ARM[MYW];armToggle();const b=ARM[MYW];armToggle();return JSON.stringify([[MYW,a,b,ARM[MYW]]]);})()"""
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
