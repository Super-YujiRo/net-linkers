exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_lib_v4.py',encoding='utf-8').read())
from mathutils import Vector,Matrix
def autorig(src_glb,out_glb,model='fumi',strip_existing_rig=True,face_dir='-Y'):
    if 'NL_AR' not in bpy.data.scenes:bpy.data.scenes.new('NL_AR')
    bpy.context.window.scene=bpy.data.scenes['NL_AR']
    for o in list(S().objects):bpy.data.objects.remove(o,do_unlink=True)
    # import target mesh
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=src_glb);new=[o for o in bpy.data.objects if o not in before]
    VL=bpy.context.view_layer.objects
    keep=[]
    for o in new:
        if o.type=='MESH' and (o.name not in VL or o.hide_get() or o.hide_render):bpy.data.objects.remove(o,do_unlink=True)
        else:keep.append(o)
    new=keep
    meshes=[o for o in new if o.type=='MESH']
    for o in new:
        if o.type=='ARMATURE' and strip_existing_rig:
            for m in meshes:
                mw=m.matrix_world.copy();m.modifiers.clear();m.parent=None;m.matrix_world=mw
            bpy.data.objects.remove(o,do_unlink=True)
    for o in list(S().objects):
        if o.type=='EMPTY':
            for c in o.children:mw=c.matrix_world.copy();c.parent=None;c.matrix_world=mw
            bpy.data.objects.remove(o,do_unlink=True)
    bpy.ops.object.select_all(action='DESELECT')
    for m in meshes:m.select_set(True)
    bpy.context.view_layer.objects.active=meshes[0]
    if len(meshes)>1:bpy.ops.object.join()
    M=bpy.context.active_object;M.name='TripoBody'
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    # face direction: our VRoid faces +Y in Blender; rotate mesh if it faces -Y
    if face_dir=='-Y':
        M.rotation_euler=(0,0,math.pi);bpy.ops.object.transform_apply(rotation=True)
    vs=[M.matrix_world@v.co for v in M.data.vertices]
    mn=Vector([min(v[i] for v in vs) for i in range(3)]);mx=Vector([max(v[i] for v in vs) for i in range(3)])
    # import VRoid rig only
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=D+'vr_'+model+'.glb');new=[o for o in bpy.data.objects if o not in before]
    arm=[o for o in new if o.type=='ARMATURE'][0]
    vms=[o for o in new if o.type=='MESH' and any(k in o.name for k in ('Body','Face','Hair'))]
    for o in new:
        if o.type=='MESH' and o not in vms:bpy.data.objects.remove(o,do_unlink=True)
    vv=[o.matrix_world@v.co for o in vms for v in o.data.vertices]
    vmn=Vector([min(v[i] for v in vv) for i in range(3)]);vmx=Vector([max(v[i] for v in vv) for i in range(3)])
    for o in vms:bpy.data.objects.remove(o,do_unlink=True)
    fz=(mx.z-mn.z)/(vmx.z-vmn.z);fx=(mx.x-mn.x)/(vmx.x-vmn.x)
    cx=(mn.x+mx.x)/2;cy=(mn.y+mx.y)/2;vcx=(vmn.x+vmx.x)/2;vcy=(vmn.y+vmx.y)/2
    # move mesh so its feet at 0 and centered like the rig
    M.location=(vcx-cx,vcy-cy,vmn.z*fz-mn.z);bpy.ops.object.select_all(action='DESELECT');M.select_set(True);bpy.context.view_layer.objects.active=M;bpy.ops.object.transform_apply(location=True)
    # fit bones: scale z by fz, arm chain x by fx (keeps arms along X)
    bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm
    bpy.ops.object.mode_set(mode='EDIT')
    for eb in arm.data.edit_bones:
        for attr in('head','tail'):
            p=getattr(eb,attr).copy()
            # bones are in armature space; armature object may have rotation/scale
            setattr(eb,attr,Vector((p.x*(fx if abs(p.x)>0.12 else fz),p.y*fz,p.z*fz)))
    bpy.ops.object.mode_set(mode='OBJECT')
    # bind with automatic weights
    bpy.ops.object.select_all(action='DESELECT');M.select_set(True);arm.select_set(True);bpy.context.view_layer.objects.active=arm
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    # export
    bpy.ops.object.select_all(action='DESELECT');M.select_set(True);arm.select_set(True);bpy.context.view_layer.objects.active=arm
    arm.data.pose_position='REST'
    bpy.ops.export_scene.gltf(filepath=out_glb,export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_skins=True,export_image_format='WEBP')
    return {'fz':fz,'fx':fx,'mesh':[list(mn),list(mx)],'vr':[list(vmn),list(vmx)]}
