exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_vir_v2.py',encoding='utf-8').read())
import random
from mathutils import Vector
def G_(c):return mat('kg'+c,c,True)
def M_(c):return mat('km'+c,c)
KITS=[]
def kit(f):KITS.append(f);return f
# every piece: group at (X,0,0); build in world coords offset by X. post: base at z=0. rail: spans x 0..1 (relative), centred y=0.
@kit
def hub(X):
    g=grp('hub_post',(X,0,0));K=M_('#1c2440');Y=G_('#ffd24a')
    vp('cyl',(.22,.22,.12),(X,0,.06),m=K,g=g,seg=6);vp('cyl',(.12,.12,.78),(X,0,.45),m=K,g=g,seg=6);vp('cyl',(.2,.2,.06),(X,0,.86),m=K,g=g,seg=6);vp('sph',(.12,.12,.12),(X,0,.95),m=Y,g=g,seg=12)
    g=grp('hub_rail',(X+1.5,0,0));vp('box',(1,.07,.07),(X+2.0,0,.4),m=K,g=g,bev=0);vp('box',(1,.04,.04),(X+2.0,0,.72),m=Y,g=g,bev=0)
    g=grp('hub_a',(X+3,0,0));vp('cyl',(.5,.5,.5),(X+3,0,.25),m=K,g=g,seg=8);vp('tor',(.45,.03),(X+3,0,1.1),m=Y,g=g);vp('box',(.7,.04,.45),(X+3,0,1.1),m=G_('#7fd8ff'),g=g,bev=0);vp('cyl',(.06,.06,.6),(X+3,0,.75),m=K,g=g)
    g=grp('hub_b',(X+4.5,0,0));vp('cyl',(.3,.3,2.6),(X+4.5,0,1.3),m=K,g=g,seg=8)
    for z in(.7,1.4,2.1):vp('tor',(.32,.035),(X+4.5,0,z),m=Y,g=g)
    vp('sph',(.2,.2,.2),(X+4.5,0,2.75),m=Y,g=g,seg=12)
@kit
def water(X):
    B=M_('#2f6fd8');W=M_('#dfe8f5');R=M_('#d83a3a');C=G_('#7fe8ff');K=M_('#1a3a7a')
    g=grp('water_post',(X,0,0));vp('cyl',(.16,.16,.85),(X,0,.42),m=B,g=g);vp('cyl',(.22,.22,.08),(X,0,.06),m=K,g=g);vp('cyl',(.2,.2,.05),(X,0,.86),m=W,g=g);vp('tor',(.16,.025),(X,0,.95),m=R,g=g);vp('box',(.3,.03,.03),(X,0,.95),m=R,g=g,bev=0);vp('box',(.03,.3,.03),(X,0,.95),m=R,g=g,bev=0)
    g=grp('water_rail',(X+1.5,0,0));vp('cyl',(.11,.11,1),(X+2.0,0,.62),rot=(0,90,0),m=W,g=g);vp('cyl',(.05,.05,1),(X+2.0,0,.28),rot=(0,90,0),m=C,g=g)
    g=grp('water_a',(X+3,0,0));vp('cyl',(1.0,1.0,1.4),(X+3,0,.7),m=W,g=g,seg=20)
    for z in(.3,.75,1.2):vp('cyl',(1.04,1.04,.08),(X+3,0,z),m=B,g=g,seg=20)
    vp('cyl',(.8,.8,.12),(X+3,0,1.45),m=K,g=g,seg=20);vp('box',(.06,.4,.8),(X+3,-.5,.75),m=C,g=g,bev=0)
    g=grp('water_b',(X+5,0,0))
    for s in(-1,1):vp('box',(.3,.4,2.2),(X+5+s*.9,0,1.1),m=K,g=g,bev=.04)
    vp('box',(2.1,.45,.3),(X+5,0,2.25),m=K,g=g,bev=.04);vp('box',(1.5,.06,1.6),(X+5,0,1.0),m=C,g=g,bev=0);vp('tor',(.25,.04),(X+5,-.3,2.25),rot=(90,0,0),m=R,g=g)
@kit
def port(X):
    Y=M_('#f0b020');K=M_('#2a2a30');O=M_('#c8501e');L=G_('#ff9a3a')
    g=grp('port_post',(X,0,0))
    for i in range(4):vp('cyl',(.26,.26,.18),(X,0,.09+i*.18),m=Y if i%2==0 else K,g=g,seg=16)
    vp('sph',(.26,.26,.16),(X,0,.75),m=Y,g=g,seg=16)
    g=grp('port_rail',(X+1.5,0,0))
    for i in range(5):vp('tor',(.07,.02),(X+1.6+i*.2,0,.55),rot=(90,0,0) if i%2 else (0,0,0),m=K,g=g,seg=4)
    g=grp('port_a',(X+3,0,0))
    for j,(dz,dx,c) in enumerate(((.6,0,O),(1.8,.2,M_('#2f6fd8')))):
        vp('box',(2.4,1.0,1.1),(X+3+dx,0,dz),m=c,g=g,bev=.03)
        for i in range(10):vp('box',(.05,1.02,1.0),(X+3+dx-1.1+i*.24,0,dz),m=K,g=g,bev=0)
    g=grp('port_b',(X+5.5,0,0));vp('box',(.35,.35,3.2),(X+5.5,0,1.6),m=Y,g=g,bev=.03)
    for i in range(6):vp('box',(.37,.37,.06),(X+5.5,0,.3+i*.5),m=K,g=g,bev=0)
    vp('box',(2.2,.25,.25),(X+6.1,0,3.25),m=Y,g=g,bev=.03);vp('cyl',(.02,.02,1.2),(X+6.9,0,2.6),m=K,g=g);vp('box',(.4,.4,.3),(X+6.9,0,1.9),m=O,g=g,bev=.03);vp('sph',(.12,.12,.12),(X+5.5,0,3.45),m=L,g=g,seg=10)
@kit
def neon(X):
    K=M_('#1a0f2a');P=G_('#ff5ad8');C=G_('#7fe8ff')
    g=grp('neon_post',(X,0,0));vp('box',(.14,.14,.95),(X,0,.47),m=K,g=g,bev=.02);vp('box',(.05,.16,.8),(X,0,.5),m=P,g=g,bev=0);vp('box',(.22,.22,.06),(X,0,.97),m=K,g=g,bev=.01)
    g=grp('neon_rail',(X+1.5,0,0));vp('cyl',(.045,.045,1),(X+2.0,0,.7),rot=(0,90,0),m=C,g=g,seg=10);vp('cyl',(.03,.03,1),(X+2.0,0,.35),rot=(0,90,0),m=P,g=g,seg=10)
    g=grp('neon_a',(X+3,0,0));vp('box',(.12,.12,2.4),(X+2.4,0,1.2),m=K,g=g,bev=.02);vp('box',(.12,.12,2.4),(X+3.6,0,1.2),m=K,g=g,bev=.02);vp('box',(1.5,.2,.9),(X+3,0,2.2),m=K,g=g,bev=.03);vp('box',(1.3,.22,.7),(X+3,0,2.2),m=P,g=g,bev=0);vp('box',(1.1,.24,.08),(X+3,0,1.85),m=C,g=g,bev=0)
    g=grp('neon_b',(X+5,0,0));vp('tor',(1.1,.07),(X+5,0,0),rot=(90,0,0),m=C,g=g,seg=36);vp('tor',(.9,.05),(X+5,0,0),rot=(90,0,0),m=P,g=g,seg=36)
@kit
def rail(X):
    K=M_('#2a3040');S=M_('#9aa4b4');GN=G_('#7dff9a');RD=G_('#ff4f5a');W=M_('#e8ecf4')
    g=grp('rail_post',(X,0,0));vp('cyl',(.1,.1,1.0),(X,0,.5),m=S,g=g);vp('box',(.22,.12,.42),(X,0,1.05),m=K,g=g,bev=.02);vp('sph',(.1,.06,.1),(X,-.07,1.15),m=GN,g=g,seg=10);vp('sph',(.1,.06,.1),(X,-.07,.95),m=RD,g=g,seg=10)
    g=grp('rail_rail',(X+1.5,0,0));vp('box',(1,.06,.08),(X+2.0,0,.12),m=S,g=g,bev=0);vp('box',(1,.06,.08),(X+2.0,0,.45),m=S,g=g,bev=0);vp('box',(.12,.1,.4),(X+2.0,0,.28),m=K,g=g,bev=0)
    g=grp('rail_a',(X+3,0,0))
    for s in(-1,1):vp('box',(.18,.18,2.8),(X+3+s*1.2,0,1.4),m=S,g=g,bev=.02)
    vp('box',(2.6,.2,.25),(X+3,0,2.8),m=S,g=g,bev=.02)
    for i,c in enumerate((GN,RD,GN)):vp('cyl',(.22,.22,.1),(X+3-.6+i*.6,-.12,2.55),rot=(90,0,0),m=c,g=g,seg=14)
    g=grp('rail_b',(X+5,0,0));vp('box',(1.4,.4,.08),(X+5,0,.45),m=W,g=g,bev=.02);vp('box',(1.4,.06,.4),(X+5,.2,.7),m=W,g=g,bev=.02)
    for s in(-1,1):vp('box',(.06,.36,.45),(X+5+s*.6,0,.22),m=K,g=g,bev=0)
@kit
def bridge(X):
    W=M_('#e8eef8');N=M_('#1a2a48');GN=G_('#7dff9a');C=G_('#9fe8ff');R=M_('#d83a3a')
    g=grp('bridge_post',(X,0,0));vp('box',(.18,.18,1.1),(X,0,.55),m=W,g=g,bev=.02);vp('box',(.26,.26,.08),(X,0,.04),m=N,g=g,bev=.01);vp('sph',(.09,.09,.09),(X,0,1.15),m=GN,g=g,seg=10)
    g=grp('bridge_rail',(X+1.5,0,0));vp('cyl',(.025,.025,1),(X+2.0,0,.95),rot=(0,90,0),m=C,g=g,seg=8);vp('box',(1,.05,.05),(X+2.0,0,.45),m=W,g=g,bev=0)
    g=grp('bridge_a',(X+3,0,0));vp('cyl',(.6,.6,.7),(X+3,0,.35),m=R,g=g,seg=16);vp('cone',(.6,.6,.5),(X+3,0,.95),m=W,g=g,seg=16);vp('sph',(.14,.14,.14),(X+3,0,1.25),m=GN,g=g,seg=10)
    g=grp('bridge_b',(X+5,0,0))
    for i in range(4):vp('cone',(1.0-i*.12,1.0-i*.12,.7,(.88-i*.12)/(1.0-i*.12)),(X+5,0,.35+i*.7),m=W if i%2==0 else R,g=g,seg=16)
    vp('cyl',(.5,.5,.35),(X+5,0,3.0),m=N,g=g,seg=12);vp('sph',(.36,.36,.36),(X+5,0,3.0),m=G_('#fff6c0'),g=g,seg=12);vp('cone',(.7,.7,.4),(X+5,0,3.35),m=R,g=g,seg=12)
@kit
def cable(X):
    K=M_('#18243e');S=M_('#5a6a88');C=G_('#3fd0ff');O=G_('#ffb040')
    g=grp('cable_post',(X,0,0));vp('box',(.32,.32,.5),(X,0,.25),m=S,g=g,bev=.04);vp('tor',(.16,.04),(X,0,.42),rot=(0,90,0),m=K,g=g);vp('sph',(.06,.06,.06),(X,-.17,.4),m=O,g=g,seg=8)
    g=grp('cable_rail',(X+1.5,0,0));vp('cyl',(.2,.2,1),(X+2.0,0,.42),rot=(0,90,0),m=K,g=g,seg=14);vp('tor',(.105,.012),(X+2.0,0,.42),rot=(0,90,0),m=C,g=g,seg=12)
    g=grp('cable_a',(X+3,0,0));vp('cyl',(1.3,1.3,.12),(X+3,-.45,.65),rot=(90,0,0),m=S,g=g,seg=24);vp('cyl',(1.3,1.3,.12),(X+3,.45,.65),rot=(90,0,0),m=S,g=g,seg=24);vp('cyl',(1.0,1.0,.8),(X+3,0,.65),rot=(90,0,0),m=K,g=g,seg=24);vp('tor',(.5,.02),(X+3,-.52,.65),rot=(90,0,0),m=C,g=g)
    g=grp('cable_b',(X+5,0,0));vp('box',(.9,.6,1.3),(X+5,0,.65),m=S,g=g,bev=.05)
    for i in range(3):vp('box',(.12,.05,.12),(X+4.75+i*.25,-.31,1.05),m=(C if i!=1 else O),g=g,bev=0)
    vp('box',(.7,.05,.5),(X+5,-.31,.55),m=K,g=g,bev=0)
@kit
def bamboo(X):
    GN=M_('#5aa04a');DG=M_('#2f6a2a');ST=M_('#8a8a80');L=G_('#ffd27a')
    g=grp('bamboo_post',(X,0,0));vp('cyl',(.12,.12,1.0),(X,0,.5),m=GN,g=g,seg=10)
    for z in(.35,.7):vp('cyl',(.135,.135,.04),(X,0,z),m=DG,g=g,seg=10)
    vp('cyl',(.12,.12,.04),(X,0,1.0),m=DG,g=g,seg=10)
    g=grp('bamboo_rail',(X+1.5,0,0));vp('cyl',(.05,.05,1),(X+2.0,0,.72),rot=(0,90,0),m=GN,g=g,seg=8);vp('cyl',(.05,.05,1),(X+2.0,0,.4),rot=(0,90,0),m=GN,g=g,seg=8)
    g=grp('bamboo_a',(X+3,0,0));random.seed(4)
    for i in range(5):
        x=X+3+random.uniform(-.5,.5);y=random.uniform(-.5,.5);h=random.uniform(3,4.6);vp('cyl',(.14,.14,h),(x,y,h/2),m=GN,g=g,seg=10)
        for z in range(1,int(h/.6)):vp('cyl',(.155,.155,.04),(x,y,z*.6),m=DG,g=g,seg=10)
        for j in range(3):vp('cone',(.5,.12,.9),(x+random.uniform(-.3,.3),y+random.uniform(-.3,.3),h-.2-j*.4),rot=(random.uniform(-40,40),random.uniform(-40,40),0),m=DG,g=g,seg=6)
    g=grp('bamboo_b',(X+5,0,0));vp('box',(.5,.5,.25),(X+5,0,.12),m=ST,g=g,bev=.03);vp('cyl',(.16,.16,.6),(X+5,0,.55),m=ST,g=g,seg=8);vp('box',(.55,.55,.4),(X+5,0,1.05),m=ST,g=g,bev=.03);vp('box',(.3,.6,.25),(X+5,0,1.05),m=L,g=g,bev=0);vp('cone',(.8,.8,.35),(X+5,0,1.42),m=ST,g=g,seg=4)
@kit
def glitch(X):
    K=M_('#1a0a2a');D=M_('#2a0a3a');P=G_('#ff5aff');C=G_('#5af0ff')
    g=grp('glitch_post',(X,0,0));vp('box',(.2,.2,.9),(X,0,.45),rot=(0,8,0),m=K,g=g,bev=.01);vp('box',(.04,.22,.5),(X+.02,0,.5),rot=(0,8,0),m=P,g=g,bev=0);vp('box',(.26,.26,.1),(X+.06,0,.93),rot=(0,-10,15),m=D,g=g,bev=0)
    g=grp('glitch_rail',(X+1.5,0,0));vp('box',(.4,.06,.06),(X+1.75,0,.55),m=K,g=g,bev=0);vp('box',(.35,.06,.06),(X+2.3,0,.6),rot=(0,6,0),m=K,g=g,bev=0);vp('box',(.15,.07,.07),(X+2.0,0,.5),m=C,g=g,bev=0)
    g=grp('glitch_a',(X+3,0,0));random.seed(9)
    for i in range(6):
        s=random.uniform(.3,.8);vp('box',(s,s,s),(X+3+random.uniform(-.7,.7),random.uniform(-.6,.6),random.uniform(.2,1.8)),rot=(random.uniform(0,90),random.uniform(0,90),0),m=random.choice((K,D)),g=g,bev=.02)
    vp('box',(1.4,.05,.05),(X+3,0,1.1),m=P,g=g,bev=0);vp('box',(.05,1.2,.05),(X+3.2,0,.6),m=C,g=g,bev=0)
    g=grp('glitch_b',(X+5,0,0));vp('cone',(.6,.6,2.4),(X+5,0,1.2),rot=(8,0,0),m=K,g=g,seg=4);vp('box',(.06,.62,1.4),(X+5,0,1.0),rot=(8,0,0),m=P,g=g,bev=0)
@kit
def core(X):
    K=M_('#1a0610');R=G_('#ff3b5c');P=G_('#ff8aa0')
    g=grp('core_post',(X,0,0));vp('cone',(.3,.3,.2,.7),(X,0,.1),m=K,g=g,seg=6);vp('cone',(.16,.16,.9),(X,0,.65),m=R,g=g,seg=6)
    g=grp('core_rail',(X+1.5,0,0));vp('box',(1,.05,.05),(X+2.0,0,.5),m=P,g=g,bev=0)
    g=grp('core_a',(X+3,0,0));random.seed(2)
    for i in range(5):
        h=random.uniform(.8,2.2);vp('cone',(.35,.35,h),(X+3+random.uniform(-.5,.5),random.uniform(-.5,.5),h/2),rot=(random.uniform(-20,20),random.uniform(-20,20),0),m=R if i%2==0 else P,g=g,seg=6)
    g=grp('core_b',(X+5,0,0));vp('box',(.7,.7,3.2),(X+5,0,1.6),m=K,g=g,bev=.04);vp('sph',(.25,.08,.25),(X+5,-.37,2.6),m=R,g=g,seg=12);vp('tor',(.32,.03),(X+5,-.37,2.6),rot=(90,0,0),m=P,g=g)
def joinmats():
    for e in [o for o in S().objects if o.type=='EMPTY' and o.name.startswith('p_')]:
        ch=[c for c in e.children if c.type=='MESH']
        bym={}
        for c in ch:bym.setdefault(c.data.materials[0].name if c.data.materials else '',[]).append(c)
        for k,L in bym.items():
            if len(L)<2:continue
            bpy.ops.object.select_all(action='DESELECT')
            for c in L:c.select_set(True)
            bpy.context.view_layer.objects.active=L[0];bpy.ops.object.join()
def kbuild():
    if 'NL_K' not in bpy.data.scenes:bpy.data.scenes.new('NL_K')
    bpy.context.window.scene=bpy.data.scenes['NL_K'];vclear()
    for i,f in enumerate(KITS):
        bpy.ops.object.select_all(action='DESELECT');f(0)
        # move groups of this kit into row i
        for o in S().objects:
            if o.type=='EMPTY' and o.name.startswith('p_') and not o.get('row'):
                o['row']=1;o.location.y+=i*4
    joinmats()
    setup_view();cam=bpy.data.objects['PCam'];cam.location=(4,-14,22);d=Vector((4,20,0))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler();cam.data.lens=28
    S().render.resolution_x=1200;S().render.resolution_y=900;S().render.filepath=D+'kits_all.png';bpy.ops.render.render(write_still=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in S().objects:
        if o.type in('MESH','EMPTY') and (o.name.startswith('p_') or o.name.startswith('m_')):o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=D+'kits.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_apply=True)
    return len([o for o in S().objects if o.type=='MESH'])
