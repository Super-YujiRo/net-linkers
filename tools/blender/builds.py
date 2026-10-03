exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_lib.py',encoding='utf-8').read())
B={}
def navihead(rig,col,acc,eye,face='#0a0c18',ears=True):
    A=mat('hA',col);C=mat('hC',acc);F=mat('hF',face);E=mat('hE',eye,True)
    prim(rig,'sph',(1.14,1.06,1.08),(0,0,1.77),m=A,bone='head',seg=32)
    prim(rig,'sph',(.86,.36,.58),(0,-.42,1.68),m=F,bone='head',seg=28)
    for s in(-1,1):
        prim(rig,'sph',(.17,.06,.21),(s*.17,-.6,1.7),m=E,bone='head',seg=14)
        if ears:
            prim(rig,'cyl',(.3,.3,.12),(s*.56,0,1.75),rot=(0,90,0),m=C,bone='head')
            prim(rig,'tor',(.1,.025),(s*.63,0,1.75),rot=(0,90,0),m=E,bone='head')
def emblem(rig,glow,dark='#0a0c18',y=-.41,z=1.0):
    prim(rig,'cyl',(.36,.36,.05),(0,y,z),rot=(90,0,0),m=mat('emD',dark))
    prim(rig,'tor',(.15,.025),(0,y-.03,z),rot=(90,0,0),m=mat('emG',glow,True))
    prim(rig,'sph',(.1,.04,.1),(0,y-.03,z),m=mat('emG',glow,True),seg=12)
def faceplate(rig,eye):
    prim(rig,'sph',(.86,.4,.7),(0,-.35,1.57),m=mat('hF','#06060c'),bone='head',seg=28)
    for s in(-1,1):prim(rig,'sph',(.15,.06,.19),(s*.16,-.52,1.64),m=mat('hE',eye,True),bone='head',seg=14)

def side(s):return 'l' if s>0 else 'r'
def b_dam():
    rig=load_body('barb');set_tex(rig,'dam');navihead(rig,'#2f6fd8','#c8d4e8','#9fe8ff')
    W=mat('wtank','#7fd8ff');MT=mat('metal','#c8d4e8');DK=mat('dk','#1a3a7a');G=mat('gl','#9fe8ff',True);BL=mat('bl','#2f6fd8')
    for s in(-1,1):
        L=side(s)
        prim(rig,'cyl',(.44,.44,1.15),(s*.34,.45,1.65),m=W,bev=.03)
        prim(rig,'cyl',(.48,.48,.09),(s*.34,.45,2.24),m=MT)
        prim(rig,'cyl',(.48,.48,.09),(s*.34,.45,1.08),m=MT)
        prim(rig,'tor',(.23,.025),(s*.34,.45,1.65),m=DK)
        prim(rig,'cyl',(.08,.08,.55),(s*.42,.2,1.35),rot=(0,s*-55,0),m=DK)
        prim(rig,'cyl',(.36,.36,.55),(s*.66,0,1.107),rot=(0,90,0),m=MT,bone='lowerarm.'+L,bev=.03)
        prim(rig,'tor',(.185,.03),(s*.5,0,1.107),rot=(0,90,0),m=BL,bone='lowerarm.'+L)
        prim(rig,'cone',(.4,.4,.2,.55),(s*1.02,0,1.107),rot=(0,s*-90,0),m=DK,bone='lowerarm.'+L)
        prim(rig,'tor',(.1,.03),(s*1.12,0,1.107),rot=(0,90,0),m=G,bone='lowerarm.'+L)
    prim(rig,'tor',(.15,.032),(0,-.42,1.02),rot=(90,0,0),m=MT)
    for a in(0,45,90,135):prim(rig,'box',(.035,.03,.3),(0,-.42,1.02),rot=(0,a,0),m=MT,bev=0)
    prim(rig,'hemi',(1.16,1.12,.95),(0,0,1.84),m=BL,bone='head')
    prim(rig,'tor',(.58,.045),(0,0,1.84),m=MT,bone='head')
    prim(rig,'box',(.12,.75,.22),(0,0,2.3),m=MT,bone='head')
    return rig
def b_dam2():
    rig=b_dam();MT=mat('metal','#c8d4e8')
    prim(rig,'tor',(.3,.05),(0,0,2.42),m=MT,bone='head')
    for a in(0,60,120):prim(rig,'box',(.6,.06,.06),(0,0,2.42),rot=(0,0,a),m=MT,bone='head',bev=0)
    prim(rig,'cyl',(.14,.14,.2),(0,0,2.35),m=MT,bone='head')
    return rig
B['dam']=b_dam2
from mathutils import Euler,Vector
def tip(c,rot,h):return tuple(Vector(c)+Euler([math.radians(x) for x in rot]).to_matrix()@Vector((0,0,h)))
def b_crane():
    rig=load_body('knight');set_tex(rig,'crane')
    Y=mat('y','#f0b020');K=mat('k','#2a2a30');GR=mat('gr','#b8bcc4');OR=mat('or','#e86a20');G=mat('lamp','#ff9a3a',True)
    navihead(rig,'#f0b020','#2a2a30','#ffe08a');emblem(rig,'#ffb040',y=-.43)
    prim(rig,'hemi',(.95,.95,.5),(0,-.05,2.45),m=Y,bone='head');prim(rig,'cyl',(1.1,1.1,.05),(0,-.08,2.45),m=Y,bone='head')
    prim(rig,'box',(.18,.18,1.7),(0,.52,1.85),m=Y);prim(rig,'box',(.3,.3,.18),(0,.52,1.08),m=K)
    prim(rig,'box',(1.9,.16,.16),(-.62,.52,2.7),m=Y)
    for i in range(5):prim(rig,'box',(.1,.17,.17),(-.1-i*.34,.52,2.7),m=K,bev=0)
    prim(rig,'box',(.45,.4,.35),(.42,.52,2.7),m=K)
    prim(rig,'sph',(.14,.14,.14),(0,.52,2.85),m=G,seg=12)
    prim(rig,'cyl',(.03,.03,.55),(-1.45,.52,2.38),m=GR)
    prim(rig,'tor',(.1,.03),(-1.45,.52,2.02),rot=(90,0,0),m=GR)
    prim(rig,'box',(.75,.45,.42),(-1.45,.52,1.7),m=OR,bev=.03)
    for i in range(3):prim(rig,'box',(.06,.47,.36),(-1.7+i*.25,.52,1.7),m=mat('or2','#b84a10'),bev=0)
    return rig
B['crane']=b_crane
def b_neon(c1='#ff5ad8',c2='#7fe8ff'):
    rig=load_body('mage',weapons=('2H_Staff',),wmat=mat('ng',c1,True));set_tex(rig,'neon');navihead(rig,'#c82a9a','#2a0a3a',c2);emblem(rig,c1)
    DK=mat('dk','#2a0a3a');P=mat('pg',c1,True);C=mat('cg',c2,True)
    for s in(-1,1):prim(rig,'cyl',(.05,.05,.35),(s*.3,0,2.3),m=DK,bone='head')
    prim(rig,'box',(1.15,.14,.48),(0,0,2.6),m=DK,bone='head',bev=.04)
    prim(rig,'box',(.98,.16,.32),(0,0,2.6),m=P,bone='head',bev=.02)
    prim(rig,'tor',(.42,.035),(0,0,1.26),m=C)
    for s in(-1,1):prim(rig,'tor',(.17,.03),(s*.36,0,1.107),rot=(0,90,0),m=P,bone='upperarm.'+side(s))
    prim(rig,'sph',(.28,.28,.28),(-.883,-1.3,1.049),m=C,bone='handslot.r',seg=16)
    return rig
B['neon']=b_neon
def b_liner():
    rig=load_body('knight');set_tex(rig,'liner')
    W=mat('w','#e8ecf4');GN=mat('gn','#3a8a3a');GL=mat('gls','#1a2430');GY=mat('gy','#5a606c');L=mat('hl','#fff6c0',True)
    navihead(rig,'#e8ecf4','#3a8a3a','#fff6c0')
    prim(rig,'box',(1.05,.68,.8),(0,-.1,.98),m=W,bev=.16)
    prim(rig,'box',(1.07,.7,.1),(0,-.1,.86),m=GN,bev=.02)
    prim(rig,'box',(.8,.06,.26),(0,-.44,1.17),m=GL,bev=.03)
    for s in(-1,1):prim(rig,'sph',(.15,.08,.15),(s*.32,-.45,.75),m=L,seg=14)
    prim(rig,'box',(.95,.24,.2),(0,-.48,.55),rot=(-35,0,0),m=GY,bone='hips')
    for s in(-1,1):prim(rig,'box',(.05,.05,.5),(s*.13,0,2.6),rot=(0,s*30,0),m=GY,bone='head')
    prim(rig,'box',(.7,.07,.05),(0,0,2.83),m=GY,bone='head')
    return rig
def b_liner2():
    rig=b_liner()
    prim(rig,'tor',(.575,.045),(0,0,1.9),m=mat('gn','#3a8a3a'),bone='head')
    prim(rig,'sph',(.14,.08,.14),(0,-.5,2.08),m=mat('hl','#fff6c0',True),bone='head',seg=12)
    return rig
B['liner']=b_liner2
def b_wave():
    rig=load_body('rogue');set_tex(rig,'wave');navihead(rig,'#2a9ad8','#e8f6ff','#bff4ff');emblem(rig,'#5ad8ff')
    W=mat('w','#e8f6ff');BL=mat('bl','#2a9ad8');C=mat('cg','#7fe8ff',True);M=mat('m','#a8c8d8')
    prim(rig,'sph',(.6,.13,1.7),(0,.42,1.55),rot=(0,14,0),m=W)
    prim(rig,'box',(.09,.15,1.35),(0,.42,1.55),rot=(0,14,0),m=C,bev=0)
    prim(rig,'cone',(.1,.6,.55),(0,.18,2.4),rot=(-18,0,0),m=BL,bone='head')
    prim(rig,'cyl',(.07,.07,1.9),(-.883,-.45,1.049),rot=(90,0,0),m=M,bone='handslot.r')
    prim(rig,'box',(.42,.06,.06),(-.883,-1.38,1.049),m=M,bone='handslot.r')
    for dx in(-.16,0,.16):prim(rig,'cone',(.1,.1,.32),(-.883+dx,-1.55,1.049),rot=(90,0,0),m=C,bone='handslot.r')
    prim(rig,'sph',(.3,.3,.3),(.883,-.12,1.049),m=C,bone='handslot.l',seg=16)
    prim(rig,'tor',(.22,.025),(.883,-.12,1.049),rot=(90,0,0),m=W,bone='handslot.l')
    return rig
def b_wave2():
    rig=b_wave()
    for s in(-1,1):prim(rig,'cone',(.08,.4,.45),(s*.6,.1,1.85),rot=(0,s*70,0),m=mat('bl','#2a9ad8'),bone='head')
    return rig
B['wave']=b_wave2
def b_shade(k='shade',c='#b98cff',sp=False):
    rig=load_body('hood',weapons=('Knife','Knife_Offhand'),wmat=mat('kg',c,True));set_tex(rig,k);navihead(rig,'#2a1a40','#120a20',c);emblem(rig,c,y=-.4)
    prim(rig,'cone',(1.0,1.0,.9),(0,.12,2.05),rot=(-25,0,0),m=mat('hood','#2a1a40'),bone='head')
    G=mat('sg',c,True);DK=mat('dk','#120a20')
    prim(rig,'tor',(.78,.03),(0,0,.85),rot=(8,0,0),m=G,bone='hips')
    prim(rig,'tor',(.62,.025),(0,0,.55),rot=(-6,0,0),m=G,bone='hips')
    for s in(-1,1):prim(rig,'cone',(.22,.22,.45),(s*.4,.05,1.36),rot=(0,s*55,0),m=DK)
    if sp:
        for i in range(5):a=math.radians(i*72);prim(rig,'cone',(.1,.1,.35),(math.sin(a)*.38,math.cos(a)*.38,2.3),rot=(math.cos(a)*-20,math.sin(a)*20,0),m=G,bone='head')
    return rig
B['shade']=b_shade
B['shadesp']=lambda:b_shade('shadesp','#ff9aff',True)
def b_hanabi():
    rig=load_body('mage',weapons=('1H_Wand',),wmat=mat('wg','#ffd24a',True));set_tex(rig,'hanabi');navihead(rig,'#d83a3a','#ffd24a','#ffd24a');emblem(rig,'#ff8a3a')
    R=mat('r','#d83a3a');W=mat('w','#f4e8d8');Y=mat('yg','#ffd24a',True);K=mat('k','#2a0a12')
    prim(rig,'tor',(.58,.06),(0,0,2.0),m=W,bone='head')
    prim(rig,'box',(.5,.3,.5),(0,.42,1.25),m=K,bev=.04)
    for i,x in enumerate((-.36,-.18,0,.18,.36)):
        rot=(-15,0,-x*50);c=(x*1.15,.48,2.0)
        prim(rig,'cyl',(.2,.2,1.05),c,rot=rot,m=R if i%2==0 else W,bev=.02)
        prim(rig,'tor',(.1,.035),tip(c,rot,.53),rot=rot,m=Y)
    return rig
def b_hanabi2():
    rig=b_hanabi()
    prim(rig,'tor',(.575,.05),(0,0,1.77),rot=(0,90,0),m=mat('w','#f4e8d8'),bone='head')
    prim(rig,'cyl',(.07,.07,.35),(0,0,2.45),rot=(10,0,0),m=mat('k','#2a0a12'),bone='head')
    prim(rig,'sph',(.16,.16,.16),(0,.03,2.65),m=mat('yg','#ffd24a',True),bone='head',seg=12)
    return rig
B['hanabi']=b_hanabi2
def b_bridge():
    rig=load_body('barb');set_tex(rig,'bamboo');navihead(rig,'#dfe4ee','#2a3a5a','#7dff9a');emblem(rig,'#7dff9a')
    W=mat('w','#dfe4ee');N=mat('n','#2a3a5a');G=mat('g','#7dff9a',True)
    prim(rig,'hemi',(1.16,1.12,.95),(0,0,1.84),m=N,bone='head');prim(rig,'tor',(.58,.045),(0,0,1.84),m=W,bone='head')
    for s in(-1,1):
        L=side(s)
        prim(rig,'box',(.5,.5,.5),(s*.62,0,1.107),m=W,bone='lowerarm.'+L,bev=.06)
        prim(rig,'box',(.52,.52,.07),(s*.62,0,1.107),rot=(0,90,0),m=G,bone='lowerarm.'+L,bev=0)
        prim(rig,'box',(.36,.46,.46),(s*.95,0,1.107),m=N,bone='lowerarm.'+L,bev=.05)
        prim(rig,'box',(.15,.15,1.05),(s*.4,.2,1.8),m=N)
        prim(rig,'sph',(.13,.13,.13),(s*.4,.2,2.36),m=G,seg=12)
    prim(rig,'box',(.95,.11,.11),(0,.2,2.12),m=W)
    prim(rig,'box',(.95,.11,.11),(0,.2,1.75),m=W)
    return rig
def b_bridge2():
    rig=b_bridge();N=mat('n','#2a3a5a');G=mat('g','#7dff9a',True)
    for s in(-1,1):
        prim(rig,'box',(.11,.11,.6),(s*.36,0,2.42),m=N,bone='head')
        prim(rig,'sph',(.1,.1,.1),(s*.36,0,2.76),m=G,bone='head',seg=10)
    prim(rig,'box',(.85,.08,.08),(0,0,2.5),m=mat('w','#dfe4ee'),bone='head')
    return rig
B['bamboo']=b_bridge2
def grab_knight_sword(rig,mt):
    before=set(bpy.data.objects);acts=set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=D+'Knight.glb')
    new=[o for o in bpy.data.objects if o not in before];sw=None
    for o in new:
        if o.type=='MESH' and base(o.name)=='2H_Sword':sw=o
    bpy.context.view_layer.update();mw=sw.matrix_world.copy()
    sw.parent=None;sw.matrix_world=mw;sw.name='NX_w_2H_Sword';sw.data.materials.clear();sw.data.materials.append(mt)
    for o in new:
        if o is not sw:bpy.data.objects.remove(o,do_unlink=True)
    for a in [a for a in bpy.data.actions if a not in acts]:bpy.data.actions.remove(a)
    pbone(sw,rig,'handslot.r');return sw
def b_blackout(k='blackout',c='#ff3b5c',sp=False):
    rig=load_body('skel');set_tex(rig,k)
    K=mat('k','#1a1a22');G=mat('bg',c,True)
    grab_knight_sword(rig,K)
    prim(rig,'box',(.07,1.35,.16),(-.883,-1.2,1.049),m=G,bone='handslot.r',bev=0)
    navihead(rig,'#1a1a22','#06060a',c,face='#000000');emblem(rig,c,y=-.4,z=1.02)
    for s in(-1,1):
        prim(rig,'cone',(.16,.16,.6),(s*.36,0,2.42),rot=(0,s*28,0),m=K,bone='head')
        prim(rig,'cone',(.2,.2,.45),(s*.42,0,1.36),rot=(0,s*65,0),m=K)
    prim(rig,'tor',(.8,.03),(0,0,.5),m=G,bone='hips')
    if sp:
        prim(rig,'tor',(.38,.04),(0,0,2.62),m=G,bone='head')
        for s in(-1,1):prim(rig,'cone',(.5,.12,1.1),(s*.55,.45,1.65),rot=(0,s*-35,0),m=G)
    return rig
B['blackout']=b_blackout
B['blackoutsp']=lambda:b_blackout('blackoutsp','#ffd24a',True)
def b_damfix():
    return b_dam()

def build(k,prev=True,exp=False):
    bpy.context.window.scene=bpy.data.scenes['NL_B2'];clear()
    rig=B[k]()
    if prev:preview(rig,k)
    if exp:export_parts(rig,k)
    return rig
def build_all(ks,exp=False):
    for k in ks:build(k,True,exp)
