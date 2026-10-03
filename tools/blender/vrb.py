exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_builds_v5.py',encoding='utf-8').read())
from mathutils import Matrix,Vector
VBM={'head':'J_Bip_C_Head','chest':'J_Bip_C_UpperChest','hips':'J_Bip_C_Hips','spine':'J_Bip_C_Spine'}
for s,SS in(('l','L'),('r','R')):
    VBM.update({'upperarm.'+s:'J_Bip_%s_UpperArm'%SS,'lowerarm.'+s:'J_Bip_%s_LowerArm'%SS,'handslot.'+s:'J_Bip_%s_Hand'%SS,'hand.'+s:'J_Bip_%s_Hand'%SS})
REF={'handslot.l':'hand.l','handslot.r':'hand.r'}
def load_vr(model):
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=D+'vr_'+model+'.glb')
    new=[o for o in bpy.data.objects if o not in before]
    arm=[o for o in new if o.type=='ARMATURE'][0];arm.name='VR_'+model
    arm.data.pose_position='REST'
    return arm,new
def bh(rig,b):return rig.matrix_world@rig.data.bones[b].head_local

PAL={'dam':('#2f6fd8','#1a3a7a','#9fd8ff'),'crane':('#e8a820','#2a2a30','#ffe08a'),'neon':('#c82a9a','#2a0a3a','#ff9ad8'),'liner':('#e8ecf4','#3a8a3a','#fff6c0'),
'wave':('#2a9ad8','#0a3a5a','#bff4ff'),'shade':('#3a2a5a','#120a20','#b98cff'),'hanabi':('#d83a3a','#2a0a12','#ffd24a'),'bamboo':('#dfe4ee','#2a3a5a','#7dff9a'),
'blackout':('#1a1a22','#06060a','#ff3b5c'),'shadesp':('#5a2a7a','#1a0a28','#ff9aff'),'blackoutsp':('#2a0a12','#06060a','#ffd24a')}
def vprim(vr,kind,dims,loc,rot=(0,0,0),m=None,bone=None,bev=.01,seg=20):
    return prim(vr,kind,dims,loc,rot=rot,m=m,bone=bone,bev=bev,seg=seg)
def armor(vr,k):
    A,Bc,C=PAL[k];MA=mat('arA',A);MB=mat('arB',Bc);MC=mat('arC',C,True)
    H=lambda b:bh(vr,b);T=lambda b:vr.matrix_world@vr.data.bones[b].tail_local
    noGaunt=k in('dam','bamboo')
    for S_,sx in(('L',-1),('R',1)):
        ua=H('J_Bip_%s_UpperArm'%S_);la=H('J_Bip_%s_LowerArm'%S_);hd=H('J_Bip_%s_Hand'%S_)
        sx=1 if ua.x>0 else -1
        vprim(vr,'hemi',(.25,.24,.2),(ua.x+sx*.03,ua.y,ua.z+.02),rot=(0,sx*25,0),m=MA,bone='J_Bip_%s_UpperArm'%S_)
        vprim(vr,'tor',(.1,.012),(ua.x+sx*.03,ua.y,ua.z+.02),rot=(0,sx*25,0),m=MC,bone='J_Bip_%s_UpperArm'%S_)
        if not noGaunt:
            L=(hd-la).length;c=la+(hd-la)*.62
            vprim(vr,'cone',(.17,.17,L*.62,.8),(c.x,c.y,c.z),rot=(0,sx*-90,0),m=MA,bone='J_Bip_%s_LowerArm'%S_)
            vprim(vr,'tor',(.065,.012),(hd.x-sx*.02,hd.y,hd.z),rot=(0,90,0),m=MC,bone='J_Bip_%s_LowerArm'%S_)
            vprim(vr,'sph',(.13,.13,.12),(hd.x+sx*.05,hd.y,hd.z),m=MB,bone='J_Bip_%s_Hand'%S_,seg=16)
        ul=H('J_Bip_%s_UpperLeg'%S_);ll=H('J_Bip_%s_LowerLeg'%S_);ft=H('J_Bip_%s_Foot'%S_)
        try:te=H('J_Bip_%s_ToeBase'%S_)
        except Exception:te=ft+Vector((0,.12,-.05))
        L=(ft-ll).length;c=ll+(ft-ll)*.6
        vprim(vr,'cone',(.19,.19,L*.75,.82),(c.x,c.y,c.z),m=MA,bone='J_Bip_%s_LowerLeg'%S_)
        vprim(vr,'tor',(.085,.014),(ll.x,ll.y,ll.z-L*.18),m=MC,bone='J_Bip_%s_LowerLeg'%S_)
        mf=(ft+te)/2
        vprim(vr,'box',(.13,.27,.1),(mf.x,mf.y+.03,ft.z-.06),m=MA,bone='J_Bip_%s_Foot'%S_,bev=.03)
        vprim(vr,'hemi',(.16,.14,.12),(ll.x,ll.y+.05,ll.z),rot=(-90,0,0),m=MB,bone='J_Bip_%s_LowerLeg'%S_)
    uc=H('J_Bip_C_UpperChest');hp=H('J_Bip_C_Hips');nk=H('J_Bip_C_Neck')
    vprim(vr,'box',(.34,.1,.2),(uc.x,uc.y+.1,uc.z+.03),m=MA,bone='J_Bip_C_UpperChest',bev=.04)
    vprim(vr,'tor',(.17,.03),(hp.x,hp.y,hp.z+.06),m=MB,bone='J_Bip_C_Hips')
    vprim(vr,'sph',(.06,.03,.06),(hp.x,hp.y+.17,hp.z+.06),m=MC,bone='J_Bip_C_Hips',seg=12)
    vprim(vr,'tor',(.085,.025),(nk.x,nk.y,nk.z+.01),m=MB,bone='J_Bip_C_Neck')
def vrbuild(k,model,prev=True,exp=True):
    bpy.context.window.scene=bpy.data.scenes['NL_B2'];clear()
    rig=B[k]();bpy.context.view_layer.update()
    vr,new=load_vr(model);bpy.context.view_layer.update()
    # measures
    top=max((o.matrix_world@Vector(c)).z for o in new if o.type=='MESH' for c in o.bound_box)
    Sh=(top-bh(vr,'J_Bip_C_Head').z)/1.07*1.05
    Sb=(bh(vr,'J_Bip_C_UpperChest').z-bh(vr,'J_Bip_C_Hips').z)/(bh(rig,'chest').z-bh(rig,'hips').z)
    Sa=(bh(vr,'J_Bip_L_Hand')-bh(vr,'J_Bip_L_LowerArm')).length/(bh(rig,'hand.l')-bh(rig,'lowerarm.l')).length
    parts=[o for o in rig.children_recursive if o.name.startswith('NX_')]
    for p in parts:
        b=p.parent_bone;rb=REF.get(b,b)
        SC=Sh*1.25 if b=='head' else (Sa*.7 if ('arm' in b or 'hand' in b) else Sb*.9)
        kb=bh(rig,rb);vb=bh(vr,VBM[b] if rb==b else VBM[rb])
        W=p.matrix_world.copy()
        RZ=Matrix.Rotation(math.pi,4,'Z')
        NW=Matrix.Translation(vb)@Matrix.Scale(SC,4)@Matrix.Translation(-(RZ@kb))@RZ@W
        p.parent=None;p.matrix_world=NW
        bpy.context.view_layer.update()
        pbone(p,vr,VBM[b])
    armor(vr,k)
    # remove kaykit rig + its meshes
    for o in list(rig.children):
        if not o.name.startswith('NX_'):bpy.data.objects.remove(o,do_unlink=True)
    bpy.data.objects.remove(rig,do_unlink=True)
    if prev:
        setup_view();cam=bpy.data.objects['PCam'];cam.location=(-1.8,4.2,1.5);d=Vector((0,0,.95))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
        S().render.filepath=D+'pv2_'+k+'.png';bpy.ops.render.render(write_still=True)
    if exp:
        bpy.ops.object.select_all(action='DESELECT');vr.select_set(True)
        for o in vr.children_recursive:
            if o.name.startswith('NX_'):o.select_set(True)
        bpy.context.view_layer.objects.active=vr
        bpy.ops.export_scene.gltf(filepath=D+'pv2_'+k+'.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_skins=True,export_apply=True)
    return {'Sh':Sh,'Sb':Sb,'Sa':Sa,'top':top}
GEN={'dam':'fumi','crane':'fumi','neon':'shino','liner':'fumi','wave':'shino','shade':'fumi','hanabi':'shino','bamboo':'fumi','blackout':'fumi','shadesp':'fumi','blackoutsp':'fumi'}
def vr_all(ks=None):
    out={}
    for k in (ks or list(GEN)):
        try:out[k]=vrbuild(k,GEN[k])
        except Exception as e:
            import traceback;out[k]=traceback.format_exc()[-600:]
    return out
