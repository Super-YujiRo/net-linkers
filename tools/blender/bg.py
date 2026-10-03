exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_vir_v2.py',encoding='utf-8').read())
import random
def Gl(c):return mat('bg',c,True)
def Mt(c):return mat('bm',c)
def bd_tower_neon(x):
    g=grp('tower_neon',(x,0,0));K=Mt('#141a33')
    vp('box',(8,8,40),(x,0,20),m=K,g=g,bev=.2)
    vp('box',(6,6,6),(x,0,43),m=K,g=g,bev=.2)
    for zz in range(4,40,3):
        for sx,sy,w,d in((0,-4.05,7,.1),(0,4.05,7,.1),(-4.05,0,.1,7),(4.05,0,.1,7)):
            if random.random()<.75:vp('box',(w,d,.35),(x+sx,sy,zz),m=Gl(random.choice(['#ffd27a','#9fe8ff','#ff9ad8'])),g=g,bev=0)
    vp('box',(.4,9.5,12),(x+4.3,0,28),m=Gl('#ff5ad8'),g=g,bev=0)
    vp('box',(.4,9.5,1),(x+4.3,0,21),m=Gl('#5ad8ff'),g=g,bev=0)
    vp('cyl',(.4,.4,10),(x,0,51),m=K,g=g)
    vp('sph',(1,1,1),(x,0,56.5),m=Gl('#ff3b5c'),g=g,seg=10)
def bd_tower_server(x):
    g=grp('tower_server',(x,0,0));K=Mt('#0e1430')
    vp('cyl',(10,10,34),(x,0,17),m=K,g=g,seg=24)
    for zz in range(3,34,4):vp('tor',(5.05,.18),(x,0,zz),m=Gl('#3fd0ff'),g=g,seg=36)
    for a in range(0,360,45):vp('box',(.3,.3,30),(x+math.cos(math.radians(a))*5.1,math.sin(math.radians(a))*5.1,17),m=Gl('#7fe8ff'),g=g,bev=0)
    vp('cone',(10,10,6,.2),(x,0,37),m=K,g=g,seg=24)
    vp('sph',(1.6,1.6,1.6),(x,0,41),m=Gl('#ffd24a'),g=g,seg=12)
def bd_data_cube(x):
    g=grp('data_cube',(x,0,0));c=Gl('#5ad8ff');s=4
    vp('box',(s*.9,s*.9,s*.9),(x,0,0),m=Mt('#0a1840'),g=g,bev=.1)
    for a in(-1,1):
        for b in(-1,1):
            vp('box',(s,.15,.15),(x,a*s/2,b*s/2),m=c,g=g,bev=0)
            vp('box',(.15,s,.15),(x+a*s/2,0,b*s/2),m=c,g=g,bev=0)
            vp('box',(.15,.15,s),(x+a*s/2,b*s/2,0),m=c,g=g,bev=0)
def bd_ring(x):
    g=grp('ring_big',(x,0,0));vp('tor',(10,.25),(x,0,0),m=Gl('#ffd24a'),g=g,seg=60);vp('tor',(8.5,.12),(x,0,0),m=Gl('#5ad8ff'),g=g,seg=60)
def bd_bridge(x):
    g=grp('bridge',(x,0,0));W=Mt('#c8d0e0');N=Mt('#1a2a48')
    vp('box',(100,6,1.2),(x,0,12),m=N,g=g,bev=.1)
    vp('box',(100,.2,.3),(x,3.1,12.3),m=Gl('#7dff9a'),g=g,bev=0)
    vp('box',(100,.2,.3),(x,-3.1,12.3),m=Gl('#ff5ad8'),g=g,bev=0)
    for tx in(-28,28):
        for sy in(-3,3):vp('box',(1.6,1.6,40),(x+tx,sy,20),m=W,g=g,bev=.2)
        vp('box',(1.6,7.6,1.6),(x+tx,0,33),m=W,g=g,bev=.2);vp('box',(1.6,7.6,1.6),(x+tx,0,24),m=W,g=g,bev=.2)
        vp('sph',(1.2,1.2,1.2),(x+tx,0,41),m=Gl('#7dff9a'),g=g,seg=10)
    for sy in(-3,3):
        pts=[(-50,13),(-28,40),(-14,24),(0,15),(14,24),(28,40),(50,13)]
        for i in range(len(pts)-1):
            a=Vector((pts[i][0],sy,pts[i][1]));b=Vector((pts[i+1][0],sy,pts[i+1][1]));m=(a+b)/2;d=b-a
            o=vp('cyl',(.3,.3,d.length),(x+m.x,m.y,m.z),m=Gl('#9fe8ff'),g=g,seg=6)
            o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    for px in range(-20,21,20):vp('box',(2,4,12),(x+px,0,6),m=N,g=g,bev=.1)
def bd_lighthouse(x):
    g=grp('lighthouse',(x,0,0))
    for i in range(6):vp('cone',(7-i*.6,7-i*.6,4,(6.4-i*.6)/(7-i*.6)),(x,0,2+i*4),m=Mt('#e8e8f0' if i%2==0 else '#d83a3a'),g=g,seg=20)
    vp('cyl',(4,4,3),(x,0,26),m=Mt('#1a2030'),g=g,seg=16);vp('sph',(3,3,3),(x,0,26),m=Gl('#fff6c0'),g=g,seg=14)
    vp('cone',(5,5,3),(x,0,29),m=Mt('#d83a3a'),g=g,seg=16)
def bd_mountain(x):
    g=grp('mountain',(x,0,0))
    for i,(dx,dy,s) in enumerate(((0,0,1),(18,6,.7),(-16,4,.8),(30,-4,.5))):
        o=vp('cone',(40*s,34*s,30*s),(x+dx,dy,15*s),m=Mt('#0c1a2a' if i%2 else '#101f33'),g=g,seg=7)
def bd_gantry(x):
    g=grp('gantry',(x,0,0));Y=Mt('#e8a820');K=Mt('#1a1a22')
    for sx in(-8,8):
        for sy in(-4,4):vp('box',(1.2,1.2,26),(x+sx,sy,13),m=Y,g=g,bev=.1)
    vp('box',(30,2,2),(x+4,0,27),m=Y,g=g,bev=.1)
    for i in range(10):vp('box',(.4,2.1,2.1),(x-10+i*3,0,27),m=K,g=g,bev=0)
    vp('box',(4,6,3),(x+12,0,24.5),m=K,g=g,bev=.1)
    vp('cyl',(.15,.15,10),(x+16,0,21),m=K,g=g,seg=6);vp('box',(5,2.4,2.4),(x+16,0,15),m=Mt('#c8501e'),g=g,bev=.1)
    vp('sph',(.6,.6,.6),(x,0,28.5),m=Gl('#ff9a3a'),g=g,seg=8)
def bd_rail(x):
    g=grp('rail_sky',(x,0,0));K=Mt('#202838')
    vp('box',(60,4,1),(x,0,14),m=K,g=g,bev=.1)
    for sy in(-1.2,1.2):vp('box',(60,.2,.2),(x,sy,14.6),m=Gl('#3fd0ff'),g=g,bev=0)
    for px in range(-24,25,12):vp('cyl',(1.6,1.6,14),(x+px,0,7),m=K,g=g,seg=10)
def bd_glitch(x):
    g=grp('glitch',(x,0,0));random.seed(7)
    for i in range(7):
        s=random.uniform(1.5,4);o=vp('box',(s,s*random.uniform(.6,1.4),s*random.uniform(.3,1)),(x+random.uniform(-6,6),random.uniform(-6,6),random.uniform(-4,6)),m=Mt(random.choice(['#1a0a2a','#2a0a3a','#0a0418'])),g=g,bev=.05)
        o.rotation_euler=(random.uniform(0,3),random.uniform(0,3),random.uniform(0,3))
        vp('box',(s*1.02,.08,.08),(x+o.location.x-x if False else o.matrix_world.translation.x,o.matrix_world.translation.y,o.matrix_world.translation.z),m=Gl(random.choice(['#b98cff','#ff5aff','#5af0ff'])),g=g,bev=0)
def bd_core(x):
    g=grp('core_orb',(x,0,0))
    vp('sph',(10,10,10),(x,0,0),m=Mt('#2a0610'),g=g,seg=24)
    vp('sph',(7,7,7),(x,0,0),m=Gl('#ff3b5c'),g=g,seg=18)
    for r,rot in((7,(70,0,0)),(7.6,(20,60,0)),(8.2,(-40,-30,0))):vp('tor',(r,.15),(x,0,0),rot=rot,m=Gl('#ff8aa0'),g=g,seg=48)
def bd_cables(x):
    g=grp('cables',(x,0,0))
    for j,(sy,col) in enumerate(((-3,'#1a2a4a'),(0,'#22324e'),(3,'#18243e'))):
        pts=[(-40,2),(-20,6+j),(0,3),(20,8-j),(40,4)]
        for i in range(len(pts)-1):
            a=Vector((pts[i][0],sy,pts[i][1]));b=Vector((pts[i+1][0],sy,pts[i+1][1]));m=(a+b)/2;d=b-a
            o=vp('cyl',(1.4,1.4,d.length+.6),(x+m.x,m.y,m.z),m=Mt(col),g=g,seg=12)
            o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
        vp('tor',(.75,.08),(x-10+j*8,sy,5),rot=(0,90,0),m=Gl('#9fe8ff'),g=g,seg=16)
BDS=[bd_tower_neon,bd_tower_server,bd_data_cube,bd_ring,bd_bridge,bd_lighthouse,bd_mountain,bd_gantry,bd_rail,bd_glitch,bd_core,bd_cables]
def bgbuild():
    random.seed(3)
    if 'NL_BG' not in bpy.data.scenes:bpy.data.scenes.new('NL_BG')
    bpy.context.window.scene=bpy.data.scenes['NL_BG'];vclear()
    for i,f in enumerate(BDS):f(i*120)
    bpy.ops.object.select_all(action='DESELECT')
    for o in S().objects:
        if o.type in('MESH','EMPTY') and (o.name.startswith('p_') or o.name.startswith('m_')):o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=D+'bd.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_apply=True)
    setup_view();cam=bpy.data.objects['PCam'];sc=S()
    shots=[]
    for i in range(len(BDS)):
        cam.location=(i*120+60,-110,40);d=Vector((i*120,0,18))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler();cam.data.lens=40;cam.data.clip_end=1000
        sc.render.filepath=D+'bd_%02d.png'%i;bpy.ops.render.render(write_still=True)
