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
bpy.context.view_layer.update()
_pl=arm.pose.bones.get('J_Bip_L_UpperArm')
_lx=(arm.matrix_world@_pl.head).x if _pl else 1
print('L_UpperArm x',round(_lx,3))
if _lx<0:
    bpy.ops.object.mode_set(mode='OBJECT')
    bs=[b for b in arm.data.bones if '_L_' in b.name or '_R_' in b.name]
    for b in bs:b.name=b.name.replace('_L_','_#L_').replace('_R_','_#R_')
    for b in bs:b.name=b.name.replace('_#L_','_R_').replace('_#R_','_L_')
    for o in me:
        for vg in o.vertex_groups:
            if '_#' in vg.name:vg.name=vg.name.replace('_#L_','_R_').replace('_#R_','_L_')
    print('swapped LR',len(bs))
    bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='POSE');bpy.context.view_layer.update()
_sg=1
for S,sx in (('L',_sg),('R',-_sg)):
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
# BACKIMG: 後頭部の「顔」を4面図の背面画像で塗り直す（正射影→UVへ書き戻し）
BI=os.environ.get('BACKIMG')
if BI:
    import numpy as np
    bpy.context.view_layer.update()
    src=bpy.data.images.load(BI);sw,sh=src.size;sp=np.array(src.pixels[:],dtype=np.float32).reshape(sh,sw,4)  # bottom-up
    msk=sp[:,:,:3].min(axis=2)<0.92;ys,xs=np.where(msk);iy0,iy1=ys.min(),ys.max();cxi=(xs.min()+xs.max())/2
    m=max(me,key=lambda o:len(o.data.vertices));mw=m.matrix_world
    V=np.array([tuple(mw@v.co) for v in m.data.vertices]);zmin,zmax=V[:,2].min(),V[:,2].max()
    nk=arm.data.bones.get('J_Bip_C_Neck');zneck=(arm.matrix_world@nk.head_local).z if nk else zmin+(zmax-zmin)*.82
    xc=(arm.matrix_world@arm.data.bones['J_Bip_C_Head'].head_local).x
    sc=(iy1-iy0)/(zmax-zmin)
    BS=float(os.environ.get('BACKSIGN','1'))  # 背中が向いている側(+y=1 / -y=-1)
    def proj(p):return cxi-BS*(p[...,0]-xc)*sc, iy0+(p[...,2]-zmin)*sc
    mat=m.active_material;_ims=[n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];tex=([i for i in _ims if 'base' in i.name.lower()]+_ims)[0]
    tw,th=tex.size;T=np.array(tex.pixels[:],dtype=np.float32).reshape(th,tw,4)
    uvl=m.data.uv_layers.active.data;N=np.array([tuple((mw.to_3x3()@p.normal).normalized()) for p in m.data.polygons])
    cnt=0
    for p in m.data.polygons:
        ny=BS*N[p.index][1]
        if ny<0.15:continue
        vs=list(p.vertices);P=V[vs]
        if P[:,2].min()<zneck-0.01*(zmax-zmin):continue
        w=min(1.0,(ny-0.15)/0.35)
        L=list(p.loop_indices);UV=np.array([tuple(uvl[l].uv) for l in L])*[tw,th]
        for k in range(1,len(L)-1):
            tri=UV[[0,k,k+1]];tp=P[[0,k,k+1]]
            x0,y0=np.floor(tri.min(0)).astype(int)-1;x1,y1=np.ceil(tri.max(0)).astype(int)+1
            gx,gy=np.meshgrid(np.arange(max(0,x0),min(tw,x1)),np.arange(max(0,y0),min(th,y1)))
            if gx.size==0:continue
            px=gx+.5;py=gy+.5;a,b,c=tri
            d=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(d)<1e-9:continue
            l1=((b[1]-c[1])*(px-c[0])+(c[0]-b[0])*(py-c[1]))/d;l2=((c[1]-a[1])*(px-c[0])+(a[0]-c[0])*(py-c[1]))/d;l3=1-l1-l2
            ins=(l1>=-.02)&(l2>=-.02)&(l3>=-.02)
            if not ins.any():continue
            wp=l1[...,None]*tp[0]+l2[...,None]*tp[1]+l3[...,None]*tp[2]
            u,v=proj(wp);ui=np.clip(u.astype(int),0,sw-1);vi=np.clip(v.astype(int),0,sh-1)
            col=sp[vi,ui,:3];gyi=gy[ins];gxi=gx[ins]
            T[gyi,gxi,:3]=T[gyi,gxi,:3]*(1-w)+col[ins]*w;cnt+=int(ins.sum())
    fp=os.path.join(os.path.dirname(os.path.abspath(dst)),'_backfixed.png')
    nim=bpy.data.images.new('basecolor_fixed',tw,th,alpha=True);nim.pixels.foreach_set(T.ravel());nim.filepath_raw=fp;nim.file_format='PNG';nim.save()
    nim2=bpy.data.images.load(fp);nim2.pack()
    for n in mat.node_tree.nodes:
        if n.type=='TEX_IMAGE' and n.image==tex:n.image=nim2
    print('backfix texels',cnt,'zneck',round(zneck,3))
DEC=int(os.environ.get('DECIM','0'))
if DEC:
    for o in me:
        nf=len(o.data.polygons)
        if nf>DEC:
            md=o.modifiers.new('dec','DECIMATE');md.ratio=DEC/nf;md.use_collapse_triangulate=True
            n=[x.name for x in o.modifiers];o.modifiers.move(n.index('dec'),0)
            bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier='dec')
            print('decim',o.name,nf,'->',len(o.data.polygons))
if os.environ.get('DRY'):sys.exit(0)
bpy.ops.export_scene.gltf(filepath=dst,export_format='GLB',export_animations=False,export_image_format='JPEG',export_jpeg_quality=88)
print('OUT',os.path.getsize(dst))
