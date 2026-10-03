exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_vir_v2.py',encoding='utf-8').read())
# reuse vp()/grp() from vir file; build props as groups p_<name> at different X so preview shows all
def G_(c):return mat('pg',c,True)
def M_(c):return mat('pm',c)
def pr_container(x):
    g=grp('container',(x,0,0));C=M_('#c8501e');D=M_('#8a3010')
    vp('box',(2.6,1.2,1.2),(x,0,0),m=C,g=g,bev=.04)
    for i in range(13):vp('box',(.06,1.22,1.1),(x-1.2+i*.2,0,0),m=D,g=g,bev=0)
    vp('box',(.04,1.0,1.0),(x+1.31,0,0),m=D,g=g,bev=0)
    for z in(-.25,.25):vp('cyl',(.03,.03,.9),(x+1.34,z,0),m=M_('#d8d8d8'),g=g)
    for sx in(-1,1):
        for sy in(-1,1):
            for sz in(-1,1):vp('box',(.12,.12,.12),(x+sx*1.25,sy*.55,sz*.55),m=M_('#3a3a40'),g=g,bev=.01)
def pr_train(x):
    g=grp('train',(x,0,0));W=M_('#e8ecf4');GN=M_('#3a8a3a');K=M_('#1a2430');Y=G_('#fff6c0')
    vp('box',(2.0,4.6,1.7),(x,-.2,.95),m=W,g=g,bev=.12)
    vp('box',(2.0,.6,1.5),(x,2.25,.85),rot=(-18,0,0),m=W,g=g,bev=.2)
    vp('box',(2.02,4.62,.35),(x,-.2,.45),m=GN,g=g,bev=0)
    vp('box',(1.6,.1,.6),(x,2.5,1.35),rot=(-18,0,0),m=K,g=g,bev=.03)
    for s in(-1,1):
        vp('sph',(.26,.12,.2),(x+s*.6,2.55,.55),m=Y,g=g,seg=14)
        for i in range(4):vp('box',(.04,.6,.5),(x+s*1.0,-1.6+i*1.0,1.25),m=K,g=g,bev=0)
        for yy in(-1.6,1.2):vp('cyl',(.5,.5,.12),(x+s*.85,yy,.1),rot=(0,90,0),m=M_('#2a2a30'),g=g)
    vp('box',(1.4,.3,.3),(x,2.45,.2),rot=(-30,0,0),m=M_('#5a606c'),g=g,bev=.03)
    vp('box',(.8,.06,.2),(x,2.42,1.82),m=G_('#ff9a3a'),g=g,bev=0)
def pr_shell(x):
    g=grp('shell',(x,0,0))
    vp('sph',(1,1,1),(x,0,0),m=M_('#d83a3a'),g=g,seg=24)
    vp('tor',(.505,.04),(x,0,0),rot=(0,90,0),m=M_('#f4e8d8'),g=g)
    vp('tor',(.505,.04),(x,0,0),rot=(90,0,0),m=M_('#f4e8d8'),g=g)
    vp('cyl',(.08,.08,.35),(x,0,.62),m=M_('#2a0a12'),g=g)
    vp('sph',(.2,.2,.2),(x,0,.82),m=G_('#ffb040'),g=g,seg=12)
def pr_drop(x):
    g=grp('drop',(x,0,0));c=G_('#7fd8ff')
    vp('sph',(1,1,1),(x,0,0),m=c,g=g,seg=20)
    vp('cone',(.72,.72,.9),(x,-.62,0),rot=(90,0,0),m=c,g=g,seg=20)
    vp('sph',(.28,.12,.22),(x+.18,.3,.3),m=G_('#ffffff'),g=g,seg=10)
def pr_shuriken(x):
    g=grp('shuriken',(x,0,0));c=M_('#3a3a48');gl=G_('#c8a0ff')
    for a in(0,90,180,270):vp('cone',(.36,.12,.75),(x+math.cos(math.radians(a))*.38,math.sin(math.radians(a))*.38,0),rot=(0,90,a),m=c,g=g,seg=4)
    vp('cyl',(.36,.36,.14),(x,0,0),m=c,g=g)
    vp('tor',(.1,.035),(x,0,0),m=gl,g=g)
def pr_bolt(x):
    g=grp('bolt',(x,0,0));c=G_('#ff5a6a')
    pts=[(0,-.5,.3),(.12,-.1,.1),(-.1,.1,.05),(.1,.5,-.25)]
    for i in range(3):
        a=Vector(pts[i]);b=Vector(pts[i+1]);m=(a+b)/2;d=b-a
        o=vp('cyl',(.12,.12,d.length),(x+m.x,m.y,m.z),m=c,g=g,seg=6)
        o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    vp('cone',(.2,.2,.3),(x+.1,.62,-.3),rot=(-90,0,0),m=c,g=g,seg=6)
def pr_nut(x):
    g=grp('nut',(x,0,0))
    vp('cyl',(1,1,.45),(x,0,0),m=M_('#9aa4b4'),g=g,seg=6,bev=.05)
    vp('cyl',(.42,.42,.5),(x,0,0),m=M_('#2a2a30'),g=g,seg=16)
def pr_neon(x):
    g=grp('neonring',(x,0,0))
    vp('tor',(.42,.09),(x,0,0),rot=(90,0,0),m=G_('#ff5ad8'),g=g)
    vp('tor',(.26,.05),(x,0,0),rot=(90,0,0),m=G_('#7fe8ff'),g=g)
def pr_wave(x):
    g=grp('wavecrest',(x,0,0));B=M_('#2a8ae8');W=M_('#e8f8ff')
    vp('cyl',(1.8,1.0,.9),(x,0,.45),rot=(0,0,0),m=B,g=g,seg=24)
    for i in range(7):vp('sph',(.36,.36,.3),(x-.75+i*.25,.25,.95),m=W,g=g,seg=12)
    vp('cone',(1.7,.6,.6),(x,.45,.95),rot=(-90,0,0),m=B,g=g,seg=20)
PROPS=[pr_container,pr_train,pr_shell,pr_drop,pr_shuriken,pr_bolt,pr_nut,pr_neon,pr_wave]
def pbuild():
    if 'NL_P' not in bpy.data.scenes:bpy.data.scenes.new('NL_P')
    bpy.context.window.scene=bpy.data.scenes['NL_P'];vclear()
    for i,f in enumerate(PROPS):f(i*3.5)
    setup_view();cam=bpy.data.objects['PCam'];cam.location=(14,-22,9);d=Vector((14,0,.5))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler();cam.data.lens=35
    S().render.resolution_x=1200;S().render.resolution_y=420
    S().render.filepath=D+'pp_all.png';bpy.ops.render.render(write_still=True)
    S().render.resolution_x=360;S().render.resolution_y=450
    bpy.ops.object.select_all(action='DESELECT')
    for o in S().objects:
        if o.type in('MESH','EMPTY') and (o.name.startswith('p_') or o.name.startswith('m_')):o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=D+'props.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_apply=True)
def pr_gate(x):
    g=grp('gate',(x,0,0));K=M_('#1c2440');Gw=G_('#dff4ff')
    R=1.75
    for i in range(8):
        a=math.radians(i*45+22.5);o=vp('box',(.42,.5,1.45),(x+math.cos(a)*R,0,1.8+math.sin(a)*R),rot=(0,-(i*45+22.5),0),m=K,g=g,bev=.05)
        vp('box',(.12,.52,.9),(x+math.cos(a)*(R-.2),0,1.8+math.sin(a)*(R-.2)),rot=(0,-(i*45+22.5),0),m=Gw,g=g,bev=0)
    for s in(-1,1):
        vp('box',(.55,.7,2.2),(x+s*2.15,0,1.1),m=K,g=g,bev=.06)
        vp('box',(.08,.72,1.6),(x+s*2.15,0,1.1),m=Gw,g=g,bev=0)
        vp('box',(.8,.9,.25),(x+s*2.15,0,.12),m=K,g=g,bev=.04)
    vp('box',(1.0,.6,.45),(x,0,3.75),m=K,g=g,bev=.06)
    vp('sph',(.26,.12,.26),(x,-.3,3.75),m=Gw,g=g,seg=12)
def pbuild2():
    if 'NL_P2' not in bpy.data.scenes:bpy.data.scenes.new('NL_P2')
    bpy.context.window.scene=bpy.data.scenes['NL_P2'];vclear()
    pr_gate(0)
    setup_view();cam=bpy.data.objects['PCam'];cam.location=(4,-9,3);d=Vector((0,0,1.8))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler();cam.data.lens=40
    S().render.filepath=D+'pp_gate.png';bpy.ops.render.render(write_still=True)
    bpy.ops.object.select_all(action='DESELECT')
    for o in S().objects:
        if o.type in('MESH','EMPTY') and (o.name.startswith('p_') or o.name.startswith('m_')):o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=D+'props2.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_apply=True)
