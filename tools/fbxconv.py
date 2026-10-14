import bpy,sys,os,re,mathutils,collections
src,dst=sys.argv[-2],sys.argv[-1];TEX=int(os.environ.get('TEX','2048'))
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=src,automatic_bone_orientation=False)
arm=[o for o in bpy.data.objects if o.type=='ARMATURE'][0];me=[o for o in bpy.data.objects if o.type=='MESH']
print('objs',[(o.name,o.type,tuple(round(x,3) for x in o.scale),tuple(round(x,3) for x in o.rotation_euler)) for o in bpy.data.objects])
m=max(me,key=lambda o:len(o.data.vertices))
cnt=collections.Counter()
for v in m.data.vertices:
    if v.groups:
        g=max(v.groups,key=lambda g:g.weight);cnt[m.vertex_groups[g.group].name]+=1
print('dom',cnt.most_common(12))
bpy.context.view_layer.update()
def wp(n):b=arm.data.bones.get(n);return tuple(round(x,3) for x in (arm.matrix_world@b.head_local)) if b else None
print('LArm',wp('mixamorig:LeftArm'),'LFore',wp('mixamorig:LeftForeArm'),'Hips',wp('mixamorig:Hips'),'Head',wp('mixamorig:Head'))
mb=[m.matrix_world@mathutils.Vector(c) for c in m.bound_box];print('meshbb',tuple(round(min(v[i] for v in mb),3) for i in range(3)),tuple(round(max(v[i] for v in mb),3) for i in range(3)))
M={'Hips':'C_Hips','Spine':'C_Spine','Spine1':'C_Chest','Spine2':'C_UpperChest','Neck':'C_Neck','Head':'C_Head'}
for S,P in (('Left','L'),('Right','R')):
    M.update({S+'Shoulder':P+'_Shoulder',S+'Arm':P+'_UpperArm',S+'ForeArm':P+'_LowerArm',S+'Hand':P+'_Hand',S+'UpLeg':P+'_UpperLeg',S+'Leg':P+'_LowerLeg',S+'Foot':P+'_Foot',S+'ToeBase':P+'_ToeBase'})
    for a,b in (('Thumb','Thumb'),('Index','Index'),('Middle','Middle'),('Ring','Ring'),('Pinky','Little')):
        for k in (1,2,3):M[S+'Hand'+a+str(k)]=P+'_'+b+str(k)
# VRMSTYLE names
for n in ('Hips','Spine','Chest','UpperChest','Neck','Head'):M[n]='C_'+n
for S,P in (('Left','L'),('Right','R')):
    for n in ('Shoulder','UpperArm','LowerArm','Hand','UpperLeg','LowerLeg','Foot'):M[S+'_'+n]=P+'_'+n
    M[S+'_Toes']=P+'_ToeBase'
    for a,b in (('Thumb','Thumb'),('Index','Index'),('Middle','Middle'),('Ring','Ring'),('Pinky','Little')):
        for k,z in ((1,'Proximal'),(2,'Intermediate'),(3,'Distal')):M[S+'_'+a+z]=P+'_'+b+str(k)
ren=0
for b in arm.data.bones:
    base=re.sub(r'^.*?:','',b.name)
    if base in M:
        nn='J_Bip_'+M[base]
        for o in me:
            vg=o.vertex_groups.get(b.name)
            if vg:vg.name=nn
        b.name=nn;ren+=1
print('renamed',ren)
# TPOSEFIX: A-pose -> T-pose (game retarget assumes T-pose rest)
import math
bpy.context.view_layer.objects.active=arm
bpy.ops.object.mode_set(mode='POSE')
def straighten(chain,target):
    for bn in chain:
        pb=arm.pose.bones.get(bn)
        if not pb:continue
        bpy.context.view_layer.update()
        h=arm.matrix_world@pb.head;t=arm.matrix_world@pb.tail;d=(t-h).normalized()
        ang=d.angle(target)
        if ang<math.radians(4):continue
        ax=d.cross(target).normalized()
        q=mathutils.Quaternion(ax,ang)
        M=arm.matrix_world.inverted()@(mathutils.Matrix.Translation(h)@q.to_matrix().to_4x4()@mathutils.Matrix.Translation(-h))@arm.matrix_world@pb.matrix
        pb.matrix=M
        print('tpose',bn,round(math.degrees(ang),1))
for S,sx in (('L',1),('R',-1)):
    straighten(['J_Bip_%s_UpperArm'%S,'J_Bip_%s_LowerArm'%S,'J_Bip_%s_Hand'%S],mathutils.Vector((sx,0,0)))
    straighten(['J_Bip_%s_UpperLeg'%S,'J_Bip_%s_LowerLeg'%S],mathutils.Vector((0,0,-1)))
bpy.context.view_layer.update()
bpy.ops.object.mode_set(mode='OBJECT')
for o in me:
    mods=[m for m in o.modifiers if m.type=='ARMATURE']
    if mods:
        bpy.context.view_layer.objects.active=o
        nm=mods[0].name;bpy.ops.object.modifier_copy(modifier=nm)
        bpy.ops.object.modifier_apply(modifier=nm)
bpy.context.view_layer.objects.active=arm
bpy.ops.object.mode_set(mode='POSE');bpy.ops.pose.select_all(action='SELECT');bpy.ops.pose.armature_apply(selected=False);bpy.ops.object.mode_set(mode='OBJECT')
for im in bpy.data.images:
    if im.size[0]>TEX:im.scale(TEX,TEX)
# DROPPBR: keep only base color (game uses map only)
for mat in bpy.data.materials:
    if mat.node_tree:
        for nd in list(mat.node_tree.nodes):
            if nd.type=='TEX_IMAGE' and nd.image and not any(k in nd.image.name.lower() for k in ('basecolor','base_color','diffuse','albedo')):mat.node_tree.nodes.remove(nd)
        for nd in mat.node_tree.nodes:
            if nd.type=='NORMAL_MAP':mat.node_tree.nodes.remove(nd);break
if os.environ.get('DRY'):sys.exit(0)
bpy.ops.export_scene.gltf(filepath=dst,export_format='GLB',export_animations=False,export_image_format='JPEG',export_jpeg_quality=88)
print('OUT',os.path.getsize(dst))
