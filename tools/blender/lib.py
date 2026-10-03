import bpy,math
from mathutils import Vector
D=r'C:\Users\LoZy\Downloads\nl_kk'+'\\'
BODYF={'knight':'Knight','barb':'Barbarian','mage':'Mage','rogue':'Rogue','hood':'Rogue_Hooded','skel':'Skeleton_Warrior'}
KEEP={'knight':['Knight_Helmet','Knight_ArmLeft','Knight_ArmRight','Knight_Body','Knight_Head','Knight_LegLeft','Knight_LegRight'],
'barb':['Barbarian_ArmLeft','Barbarian_ArmRight','Barbarian_Body','Barbarian_LegLeft','Barbarian_LegRight'],
'mage':['Mage_ArmLeft','Mage_ArmRight','Mage_Body','Mage_LegLeft','Mage_LegRight'],
'rogue':['Rogue_ArmLeft','Rogue_ArmRight','Rogue_Body','Rogue_LegLeft','Rogue_LegRight'],
'hood':['Rogue_Cape','Rogue_ArmLeft','Rogue_ArmRight','Rogue_Body','Rogue_Head_Hooded','Rogue_LegLeft','Rogue_LegRight'],
'skel':['Skeleton_Warrior_Helmet','Skeleton_Warrior_ArmLeft','Skeleton_Warrior_ArmRight','Skeleton_Warrior_Body','Skeleton_Warrior_Cloak','Skeleton_Warrior_Eyes','Skeleton_Warrior_Head','Skeleton_Warrior_Jaw','Skeleton_Warrior_LegLeft','Skeleton_Warrior_LegRight']}
def S():return bpy.context.scene
def base(n):return n.split('.')[0]
def clear():
    for o in list(S().objects):
        if o.type in('MESH','ARMATURE','EMPTY'):bpy.data.objects.remove(o,do_unlink=True)
    for m in list(bpy.data.meshes):
        if m.users==0:bpy.data.meshes.remove(m)
    for a in list(bpy.data.actions):
        if a.users==0:bpy.data.actions.remove(a)
def load_body(body,weapons=(),wmat=None):
    before=set(bpy.data.objects);acts=set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=D+BODYF[body]+'.glb')
    new=[o for o in bpy.data.objects if o not in before]
    rig=[o for o in new if o.type=='ARMATURE'][0]
    for o in new:
        if o.type!='MESH':continue
        b=base(o.name)
        if b in KEEP[body]:continue
        if b in weapons:
            o.name='NX_w_'+b;o.data.materials.clear();o.data.materials.append(wmat[b] if isinstance(wmat,dict) else wmat);continue
        bpy.data.objects.remove(o,do_unlink=True)
    idle=None
    for a in [a for a in bpy.data.actions if a not in acts]:
        if idle is None and base(a.name)=='Idle':idle=a
        else:bpy.data.actions.remove(a)
    if rig.animation_data is None:rig.animation_data_create()
    rig.animation_data.action=idle
    rig.data.pose_position='REST'
    return rig
def set_tex(rig,k):
    img=bpy.data.images.load(D+'b2_'+k+'.png',check_existing=True)
    for o in rig.children:
        if o.type=='MESH' and not o.name.startswith('NX_'):
            for ms in o.material_slots:
                if ms.material and ms.material.node_tree:
                    for n in ms.material.node_tree.nodes:
                        if n.type=='TEX_IMAGE':n.image=img
def mat(n,col,glow=False):
    nm=('NX_g_' if glow else 'NX_m_')+n+col
    m=bpy.data.materials.get(nm)
    if m:return m
    m=bpy.data.materials.new(nm);m.use_nodes=True;b=m.node_tree.nodes['Principled BSDF']
    c=[int(col[i:i+2],16)/255 for i in (1,3,5)];lin=tuple(x**2.2 for x in c)+(1,)
    if glow:
        b.inputs['Base Color'].default_value=(0,0,0,1);b.inputs['Emission Color'].default_value=lin;b.inputs['Emission Strength'].default_value=4
    else:
        b.inputs['Base Color'].default_value=lin;b.inputs['Roughness'].default_value=.45;b.inputs['Metallic'].default_value=0
    return m
def pbone(o,rig,bone):
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
    rig.data.bones.active=rig.data.bones[bone]
    bpy.ops.object.parent_set(type='BONE',keep_transform=True)
def prim(rig,kind,dims,loc,rot=(0,0,0),m=None,bone='chest',bev=.02,seg=20):
    if kind=='box':bpy.ops.mesh.primitive_cube_add(size=1)
    elif kind=='cyl':bpy.ops.mesh.primitive_cylinder_add(vertices=seg,radius=.5,depth=1)
    elif kind=='cone':bpy.ops.mesh.primitive_cone_add(vertices=seg,radius1=.5,radius2=(dims[3] if len(dims)>3 else 0)*.5,depth=1)
    elif kind=='sph':bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=max(6,seg//2),radius=.5)
    elif kind=='tor':bpy.ops.mesh.primitive_torus_add(major_segments=seg+12,minor_segments=8,major_radius=dims[0],minor_radius=dims[1])
    elif kind=='hemi':
        bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=max(6,seg//2),radius=.5)
        import bmesh;o=bpy.context.active_object;bm=bmesh.new();bm.from_mesh(o.data)
        bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.z<-0.001],context='VERTS');bm.to_mesh(o.data);bm.free()
    elif kind=='wedge':
        bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.707,radius2=0,depth=1)
    o=bpy.context.active_object;o.name='NX_'+kind
    if kind!='tor':o.scale=dims[:3]
    o.rotation_euler=[math.radians(x) for x in rot];o.location=loc
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bev and kind in('box','cyl'):
        md=o.modifiers.new('bv','BEVEL');md.width=bev;md.segments=2;md.limit_method='ANGLE'
        bpy.ops.object.modifier_apply(modifier='bv')
    try:bpy.ops.object.shade_smooth_by_angle()
    except Exception:bpy.ops.object.shade_smooth()
    if m:o.data.materials.append(m)
    pbone(o,rig,bone);return o
def eyes(rig,col,y=-.47,z=1.58,x=.15,r=.07):
    g=mat('eye',col,True)
    for s in(-1,1):prim(rig,'sph',(r,r*.6,r*1.2),(s*x,y,z),m=g,bone='head',seg=12)
def setup_view():
    sc=S();cam=bpy.data.objects.get('PCam')
    if cam is None:
        cam=bpy.data.objects.new('PCam',bpy.data.cameras.new('PCam'))
    if cam.name not in sc.objects:sc.collection.objects.link(cam)
    cam.location=(2.9,-6.2,2.4);d=Vector((0,0,1.4))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler();cam.data.lens=58;sc.camera=cam
    sun=bpy.data.objects.get('PSun')
    if sun is None:
        sun=bpy.data.objects.new('PSun',bpy.data.lights.new('PSun','SUN'));sun.data.energy=3.5;sun.rotation_euler=(math.radians(50),0,math.radians(30))
    if sun.name not in sc.objects:sc.collection.objects.link(sun)
    if sc.world is None:sc.world=bpy.data.worlds.new('PW')
    sc.world.use_nodes=True;bg=sc.world.node_tree.nodes.get('Background')
    if bg:bg.inputs[0].default_value=(.42,.44,.5,1);bg.inputs[1].default_value=1
    for e in('BLENDER_EEVEE','BLENDER_EEVEE_NEXT'):
        try:sc.render.engine=e;break
        except Exception:pass
    sc.render.resolution_x=360;sc.render.resolution_y=450;sc.render.resolution_percentage=100
def preview(rig,k,frame=12):
    setup_view();rig.data.pose_position='POSE';S().frame_set(frame)
    S().render.filepath=D+'p2_'+k+'.png';bpy.ops.render.render(write_still=True)
    rig.data.pose_position='REST';S().frame_set(0)
def export_parts(rig,k):
    rig.data.pose_position='REST'
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
    for o in rig.children_recursive:
        if o.name.startswith('NX_'):o.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.gltf(filepath=D+'p2_'+k+'.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_skins=True,export_apply=True)
def export_body(rig,body):
    rig.data.pose_position='REST'
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True)
    for o in rig.children:
        if o.type=='MESH' and not o.name.startswith('NX_'):o.select_set(True)
    bpy.context.view_layer.objects.active=rig
    bpy.ops.export_scene.gltf(filepath=D+'body_'+body+'.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_image_format='WEBP',export_apply=True)
