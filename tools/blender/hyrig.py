import bpy,numpy as np,math,os
from mathutils import Vector,Matrix
D=r'C:\Users\LoZy\Downloads\nl_kk\\'
def _mesh_np(o):
    me=o.data;co=np.empty(len(me.vertices)*3,np.float32);me.vertices.foreach_get('co',co);return co.reshape(-1,3)
def segdist(P,a,b):
    ab=b-a;t=np.clip(((P-a)@ab)/max(ab@ab,1e-9),0,1);return np.linalg.norm(P-(a+t[:,None]*ab),axis=1)
def rot_between(u,v):
    u=u/np.linalg.norm(u);v=v/np.linalg.norm(v);c=float(u@v);ax=np.cross(u,v);s=np.linalg.norm(ax)
    if s<1e-8:
        if c>0:return np.eye(3)
        p=np.array([1,0,0]) if abs(u[0])<.9 else np.array([0,1,0]);ax=np.cross(u,p);ax/=np.linalg.norm(ax);return np.array(Matrix.Rotation(math.pi,3,Vector(ax)))
    return np.array(Matrix.Rotation(math.atan2(s,c),3,Vector(ax/s)))
def hyrig(key,src,LM,tris=24000,tex=1024,fixed_tex=None,keep_maps=False,extra_rules=None):
    """LM: landmarks in source coords (front=-Y, character-left=+X)."""
    if 'NL_RIG' not in bpy.data.scenes:bpy.data.scenes.new('NL_RIG')
    sc=bpy.data.scenes['NL_RIG'];bpy.context.window.scene=sc
    for o in list(sc.objects):bpy.data.objects.remove(o,do_unlink=True)
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=src);new=[o for o in bpy.data.objects if o not in before]
    ms=[o for o in new if o.type=='MESH'];M=ms[0]
    for o in new:
        if o is not M:bpy.data.objects.remove(o,do_unlink=True)
    bpy.ops.object.select_all(action='DESELECT');M.select_set(True);bpy.context.view_layer.objects.active=M
    M.parent=None;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    # decimate
    r=min(1.0,tris/len(M.data.polygons))
    if r<1:
        md=M.modifiers.new('dec','DECIMATE');md.ratio=r;bpy.ops.object.modifier_apply(modifier=md.name)
    # rotate so front=+Y (fumi convention); landmarks (x,y,z)->(-x,-y,z)
    V=_mesh_np(M);V[:,0]*=-1;V[:,1]*=-1
    def p(t):return np.array([-t[0],-t[1],t[2]],float)
    J={}
    J['hips']=p((0,LM['hips'][1],LM['hips'][0]));J['spine']=p((0,LM['hips'][1],LM['spine']))
    J['chest']=p((0,LM['hips'][1],LM['chest']));J['uchest']=p((0,LM['hips'][1],LM['uchest']))
    J['neck']=p((0,LM['hips'][1],LM['neck']));J['head']=p((0,LM['hips'][1],LM['head']));J['top']=p((0,LM['hips'][1],LM['top']))
    for s,sg in(('L',1),('R',-1)):
        for n in('sh','el','ha','hp','kn','an','toe'):
            t=LM[n];J[s+n]=p((sg*t[0],t[1],t[2]))
        t=LM.get('tip',LM['ha']);J[s+'tip']=p((sg*t[0],t[1],t[2]))
    # posed segments (bone name, head, tail)
    segs=[('J_Bip_C_Hips','hips','spine'),('J_Bip_C_Spine','spine','chest'),('J_Bip_C_Chest','chest','uchest'),('J_Bip_C_UpperChest','uchest','neck'),('J_Bip_C_Neck','neck','head'),('J_Bip_C_Head','head','top')]
    for s in 'LR':
        segs+=[('J_Bip_%s_UpperArm'%s,s+'sh',s+'el'),('J_Bip_%s_LowerArm'%s,s+'el',s+'ha'),('J_Bip_%s_Hand'%s,s+'ha',s+'tip'),
               ('J_Bip_%s_UpperLeg'%s,s+'hp',s+'kn'),('J_Bip_%s_LowerLeg'%s,s+'kn',s+'an'),('J_Bip_%s_Foot'%s,s+'an',s+'toe')]
    # T-pose joints: same hips/spine; arms straight along fumi dir; legs straight down
    T=dict(J)
    for s,sx in(('L',-1),('R',1)):
        sh=J[s+'sh'];l1=np.linalg.norm(J[s+'el']-sh);l2=np.linalg.norm(J[s+'ha']-J[s+'el']);l3=np.linalg.norm(J[s+'tip']-J[s+'ha'])
        d=np.array([sx,0,-0.02]);d/=np.linalg.norm(d)
        T[s+'el']=sh+d*l1;T[s+'ha']=T[s+'el']+d*l2;T[s+'tip']=T[s+'ha']+d*max(l3,0.01)
        hp=J[s+'hp'];k1=np.linalg.norm(J[s+'kn']-hp);k2=np.linalg.norm(J[s+'an']-J[s+'kn'])
        T[s+'kn']=hp+np.array([0,0,-k1]);T[s+'an']=T[s+'kn']+np.array([0,0,-k2])
        T[s+'toe']=T[s+'an']+(J[s+'toe']-J[s+'an'])
    # assignment
    names=[g[0] for g in segs];Dm=np.stack([segdist(V,J[a],J[b]) for _,a,b in segs],1)
    # bias: torso slightly preferred, hands preferred over lower arm only near tip
    bias=np.array([1.0 if 'C_' in n else 1.0 for n in names]);Dm=Dm*bias
    if extra_rules:Dm=extra_rules(V,J,names,Dm)
    asg=np.argmin(Dm,1)
    # head rule
    hi=names.index('J_Bip_C_Head');ni=names.index('J_Bip_C_Neck')
    arm_ids=[i for i,n in enumerate(names) if 'Arm' in n or 'Hand' in n]
    headr=LM.get('head_r',0.12)
    m=(V[:,2]>J['neck'][2]+0.01)&(np.hypot(V[:,0],V[:,1]-J['head'][1])<headr);asg[m]=hi
    # transform each vertex rigidly from posed to T
    VT=V.copy()
    for i,(n,a,b) in enumerate(segs):
        sel=asg==i
        if not sel.any():continue
        R=rot_between(J[b]-J[a],T[b]-T[a])
        VT[sel]=(V[sel]-J[a])@R.T+T[a]
    me=M.data;me.vertices.foreach_set('co',VT.ravel());me.update()
    # armature from fumi
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=D+'vr_fumi.glb');new=[o for o in bpy.data.objects if o not in before]
    arm=[o for o in new if o.type=='ARMATURE'][0]
    for o in new:
        if o.type=='MESH':bpy.data.objects.remove(o,do_unlink=True)
    bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm
    fz=(T['top'][2])/1.79
    bpy.ops.object.mode_set(mode='EDIT');eb=arm.data.edit_bones
    fum={b.name:(b.head.copy(),b.tail.copy()) for b in eb}
    newh={}
    for n,a,b in segs:newh[n]=Vector(T[a])
    newh['J_Bip_L_ToeBase']=Vector(T['Ltoe']);newh['J_Bip_R_ToeBase']=Vector(T['Rtoe'])
    for s in 'LR':newh['J_Bip_%s_Shoulder'%s]=Vector((T['uchest']+T[s+'sh'])/2)
    def place(b):
        if b.name in newh:h=newh[b.name]
        else:
            pa=b.parent;ph=place.done[pa.name] if pa else Vector((0,0,0))
            h=ph+(fum[b.name][0]-fum[pa.name][0])*fz if pa else fum[b.name][0]*fz
        place.done[b.name]=h;return h
    place.done={}
    order=[];st=[b for b in eb if b.parent is None]
    while st:
        b=st.pop(0);order.append(b);st+=list(b.children)
    for b in order:
        h=place(b);L=(fum[b.name][1]-fum[b.name][0]).length*fz
        b.head=h;b.tail=h+Vector((0,0,max(L,0.005)))
    bpy.ops.object.mode_set(mode='OBJECT')
    # weights
    for g in list(M.vertex_groups):M.vertex_groups.remove(g)
    for i,n in enumerate(names):
        idx=np.where(asg==i)[0].tolist()
        if idx:M.vertex_groups.new(name=n).add(idx,1.0,'REPLACE')
    M.parent=arm;mod=M.modifiers.new('Armature','ARMATURE');mod.object=arm
    # material: base color only, shrink
    mat=M.data.materials[0];nt=mat.node_tree;bsdf=[n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'][0]
    lk=bsdf.inputs['Base Color'].links;img=lk[0].from_node.image
    if fixed_tex:img=bpy.data.images.load(fixed_tex,check_existing=False);lk[0].from_node.image=img
    im2=img.copy();im2.name='hy_%s_base'%key;im2.scale(tex,tex);lk[0].from_node.image=im2
    if not keep_maps:
        for inp in('Metallic','Roughness','Normal'):
            for l in list(bsdf.inputs[inp].links):nt.links.remove(l)
        bsdf.inputs['Metallic'].default_value=0.0;bsdf.inputs['Roughness'].default_value=0.6
    M.name='hy_'+key
    bpy.ops.object.select_all(action='DESELECT');M.select_set(True);arm.select_set(True);bpy.context.view_layer.objects.active=arm
    out=D+'hyr_%s.glb'%key
    bpy.ops.export_scene.gltf(filepath=out,export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_skins=True,export_image_format='WEBP',export_image_quality=88)
    cnt={n:int((asg==i).sum()) for i,n in enumerate(names)}
    return {'out':out,'size':os.path.getsize(out),'tris':len(M.data.polygons),'cnt':cnt,'fz':fz}
