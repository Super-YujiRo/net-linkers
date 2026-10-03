exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_lib_v3.py',encoding='utf-8').read())
from mathutils import Vector
def grp(name,loc):
    e=bpy.data.objects.new('p_'+name,None);S().collection.objects.link(e);e.location=loc;return e
def vp(kind,dims,loc,rot=(0,0,0),m=None,g=None,bev=.02,seg=24):
    if kind=='box':bpy.ops.mesh.primitive_cube_add(size=1)
    elif kind=='cyl':bpy.ops.mesh.primitive_cylinder_add(vertices=seg,radius=.5,depth=1)
    elif kind=='cone':bpy.ops.mesh.primitive_cone_add(vertices=seg,radius1=.5,radius2=(dims[3] if len(dims)>3 else 0)*.5,depth=1)
    elif kind in('sph','hemi'):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=max(8,seg//2),radius=.5)
        if kind=='hemi':
            import bmesh;o=bpy.context.active_object;bm=bmesh.new();bm.from_mesh(o.data)
            bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.z<-0.001],context='VERTS');bm.to_mesh(o.data);bm.free()
    elif kind=='tor':bpy.ops.mesh.primitive_torus_add(major_segments=seg+12,minor_segments=10,major_radius=dims[0],minor_radius=dims[1])
    o=bpy.context.active_object;o.name='m_'+kind
    if kind!='tor':o.scale=dims[:3]
    o.rotation_euler=[math.radians(x) for x in rot];o.location=loc
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bev and kind in('box','cyl'):
        md=o.modifiers.new('bv','BEVEL');md.width=bev;md.segments=3;md.limit_method='ANGLE';bpy.ops.object.modifier_apply(modifier='bv')
    try:bpy.ops.object.shade_smooth_by_angle()
    except Exception:bpy.ops.object.shade_smooth()
    if m:o.data.materials.append(m)
    if g:
        mw=o.matrix_world.copy();o.parent=g;o.matrix_world=mw
    return o
def vclear():
    for o in list(S().objects):
        if o.type in('MESH','EMPTY'):bpy.data.objects.remove(o,do_unlink=True)
def v_bitton():
    BL=mat('vb','#46a8f5');LB=mat('vlb','#bfe6ff');Y=mat('vy','#ffd23a');K=mat('vk','#2a2a30');MT=mat('vm','#9aa4b4');WD=mat('vw','#a8703a');G=mat('vg','#fff2a0',True);BO=mat('vbo','#3a4a6a')
    core=grp('core',(0,0,.55))
    vp('sph',(.86,.8,.8),(0,0,.52),m=BL,g=core)
    vp('sph',(.5,.2,.4),(0,-.32,.45),m=LB,g=core)
    vp('hemi',(.98,.94,.8),(0,.02,.66),m=Y,g=core)
    vp('cyl',(1.04,1.0,.06),(0,-.04,.66),m=Y,g=core,bev=.015)
    vp('box',(.12,.9,.06),(0,0,.98),rot=(0,0,0),m=K,g=core,bev=.01)
    vp('cyl',(.16,.16,.08),(0,-.44,.86),rot=(90,0,0),m=K,g=core)
    vp('sph',(.12,.06,.12),(0,-.49,.86),m=G,g=core,seg=12)
    ham=grp('hammer',(.46,-.05,.55))
    vp('cyl',(.07,.07,.62),(.46,-.05,.84),m=WD,g=ham)
    vp('box',(.4,.22,.22),(.46,-.05,1.15),rot=(0,0,0),m=MT,g=ham,bev=.03)
    vp('cyl',(.24,.24,.04),(.26,-.05,1.15),rot=(0,90,0),m=K,g=ham)
    vp('cyl',(.24,.24,.04),(.66,-.05,1.15),rot=(0,90,0),m=K,g=ham)
    for s,n in((-1,'footL'),(1,'footR')):
        f=grp(n,(s*.2,0,.12))
        vp('sph',(.24,.32,.18),(s*.2,-.05,.1),m=BO,g=f)
def v_phantom():
    P=mat('vp','#a47cff');L=mat('vpl','#d8c4ff');D=mat('vpd','#4a2a8a');G=mat('vpg','#ff7ae0',True)
    core=grp('core',(0,0,1.0))
    vp('sph',(.9,.84,.9),(0,0,1.12),m=P,g=core,seg=28)
    vp('cone',(1.0,.94,.8,.84),(0,0,.82),m=P,g=core,seg=28)
    for i in range(8):
        a=math.radians(i*45);vp('cone',(.24,.24,.28),(math.sin(a)*.42,math.cos(a)*.4,.34),rot=(180,0,0),m=P,g=core,seg=12)
    for s in(-1,1):vp('cone',(.2,.2,.42),(s*.5,-.05,.95),rot=(0,s*-70,0),m=L,g=core,seg=14)
    vp('sph',(.2,.12,.16),(0,-.45,.92),m=D,g=core,seg=14)
def vexport(k):
    bpy.ops.object.select_all(action='DESELECT')
    for o in S().objects:
        if o.type in('MESH','EMPTY') and (o.name.startswith('p_') or o.name.startswith('m_')):o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=D+'vir_'+k+'.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_apply=True)
def vprev(k):
    setup_view();cam=bpy.data.objects['PCam'];cam.location=(2.2,-4.6,2.0);d=Vector((0,0,.75))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    S().render.filepath=D+'pv_'+k+'.png';bpy.ops.render.render(write_still=True)
def vbuild(k):
    if 'NL_V' not in bpy.data.scenes:bpy.data.scenes.new('NL_V')
    bpy.context.window.scene=bpy.data.scenes['NL_V'];vclear()
    {'bitton':v_bitton,'phantom':v_phantom}[k]();vprev(k);vexport(k)
