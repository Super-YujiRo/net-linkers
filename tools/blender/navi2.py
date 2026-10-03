exec(open(r'C:\Users\LoZy\Downloads\nl_kk\nl_lib_v4.py',encoding='utf-8').read())
from mathutils import Vector,Matrix,Euler
GEN={'dam':'fumi','crane':'fumi','neon':'shino','liner':'fumi','wave':'shino','shade':'fumi','hanabi':'shino','bamboo':'fumi','blackout':'fumi','shadesp':'fumi','blackoutsp':'fumi'}
V={}
def bj(n):return 'J_Bip_'+n
def setupv(model):
    if 'NL_V2' not in bpy.data.scenes:bpy.data.scenes.new('NL_V2')
    bpy.context.window.scene=bpy.data.scenes['NL_V2']
    for o in list(S().objects):
        if o.type in('MESH','ARMATURE','EMPTY'):bpy.data.objects.remove(o,do_unlink=True)
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=D+'vr_'+model+'.glb')
    new=[o for o in bpy.data.objects if o not in before];vr=[o for o in new if o.type=='ARMATURE'][0];vr.data.pose_position='REST'
    V['vr']=vr;V['meshes']=[o for o in new if o.type=='MESH']
    P=lambda b:vr.matrix_world@vr.data.bones[bj(b)].head_local
    V['s']=(P('C_Neck').z-P('C_Hips').z)/0.448
    return vr
def P(b):vr=V['vr'];return vr.matrix_world@vr.data.bones[bj(b)].head_local
def at(b,o=(0,0,0)):return P(b)+Vector(o)*V['s']
def pt(kind,dims,b,o=(0,0,0),rot=(0,0,0),m=None,bone=None,bev=.008,seg=20):
    s=V['s'];d=tuple(x*s for x in dims)
    return prim(V['vr'],kind,d,tuple(at(b,o)),rot=rot,m=m,bone=bj(bone or b),bev=bev*s,seg=seg)
def G(c):return mat('g',c,True)
def M(c):return mat('m',c)
SIDES=(('L',-1),('R',1))
def boots(A,Bc,C):
    for S_,sx in SIDES:
        ll=P(S_+'_LowerLeg');ft=P(S_+'_Foot');te=P(S_+'_ToeBase');s=V['s']
        L=(ft-ll).length/s;c=(ll+(ft-ll)*.6-P(S_+'_LowerLeg'))/s
        pt('cone',(.19,.19,L*.75,.82),S_+'_LowerLeg',tuple(c),m=M(A))
        pt('tor',(.085,.014),S_+'_LowerLeg',(0,0,-L*.18),m=G(C))
        mf=((ft+te)/2-ft)/s
        pt('box',(.13,.27,.1),S_+'_Foot',(mf.x,mf.y+.03,-.06),m=M(A),bev=.03)
        pt('hemi',(.16,.14,.12),S_+'_LowerLeg',(0,.05,0),rot=(-90,0,0),m=M(Bc))
def belt(Bc,C):
    pt('tor',(.17,.03),'C_Hips',(0,0,.06),m=M(Bc));pt('sph',(.06,.03,.06),'C_Hips',(0,.17,.06),m=G(C),seg=12)
def eyes2(b,c,y,z,x=.055,r=.05,bone=None):
    for sx in(-1,1):pt('sph',(r,r*.5,r*1.2),b,(sx*x,y,z),m=G(c),bone=bone,seg=12)
def side_off(S_):return -1 if S_=='L' else 1
def arm_len(S_):return (P(S_+'_Hand')-P(S_+'_LowerArm')).length/V['s']
# ---------- designs ----------
def d_dam():
    A,Bc,C,MT='#2f6fd8','#1a3a7a','#9fe8ff','#c8d4e8'
    pt('cyl',(.3,.3,.26),'C_Head',(0,0,.12),m=M(A),bone='C_Neck',bev=.03)
    pt('box',(.24,.05,.12),'C_Head',(0,.14,.11),m=M('#0a0c18'),bone='C_Neck',bev=.02)
    eyes2('C_Head',C,.165,.11,bone='C_Neck')
    pt('tor',(.15,.025),'C_Head',(0,0,.3),m=M(MT),bone='C_Neck')
    for a in(0,60,120):pt('box',(.3,.03,.03),'C_Head',(0,0,.3),rot=(0,0,a),m=M(MT),bone='C_Neck',bev=0)
    pt('cyl',(.06,.06,.08),'C_Head',(0,0,.27),m=M(MT),bone='C_Neck')
    pt('box',(.5,.26,.36),'C_UpperChest',(0,.02,-.02),m=M(A),bev=.03)
    for x in(-.15,-.05,.05,.15):pt('box',(.04,.02,.24),'C_UpperChest',(x,.15,-.02),m=G(C),bev=0)
    pt('cyl',(.28,.28,.55),'C_UpperChest',(0,-.22,.02),m=M('#7fd8ff'),bev=.02)
    for z in(-.26,.3):pt('cyl',(.31,.31,.05),'C_UpperChest',(0,-.22,z),m=M(MT))
    for S_,sx in SIDES:
        L=arm_len(S_)
        pt('cyl',(.15,.15,L*.9),S_+'_LowerArm',(sx*L*.5,0,0),rot=(0,90,0),m=M(Bc))
        for f in(.2,.45,.7):pt('tor',(.08,.018),S_+'_LowerArm',(sx*L*f,0,0),rot=(0,90,0),m=M(A))
        pt('cone',(.2,.2,.16,.55),S_+'_LowerArm',(sx*(L+.07),0,0),rot=(0,sx*-90,0),m=M(MT))
        pt('tor',(.06,.015),S_+'_LowerArm',(sx*(L+.15),0,0),rot=(0,90,0),m=G(C))
        pt('hemi',(.2,.2,.14),S_+'_UpperArm',(sx*.03,0,.03),rot=(0,sx*25,0),m=M(A))
    boots(A,Bc,C);belt(Bc,C)
    return ['C_Head','L_Hand','R_Hand']
def d_crane():
    A,Bc,C,O='#f0b020','#2a2a30','#ffe08a','#e86a20'
    pt('box',(.3,.28,.28),'C_Head',(0,0,.12),m=M(A),bone='C_Neck',bev=.03)
    pt('box',(.26,.04,.14),'C_Head',(0,.13,.14),m=M('#1a2a3a'),bone='C_Neck',bev=.01)
    eyes2('C_Head',C,.155,.14,bone='C_Neck')
    pt('sph',(.07,.07,.07),'C_Head',(0,0,.29),m=G('#ff9a3a'),bone='C_Neck',seg=12)
    for sx in(-1,1):
        for i in range(3):pt('box',(.02,.29,.04),'C_Head',(sx*.151,0,.04+i*.08),m=M(Bc),bone='C_Neck',bev=0)
    L=arm_len('R')
    pt('box',(.95,.1,.1),'R_LowerArm',(.45,0,.02),m=M(A),bev=.01)
    for i in range(6):pt('box',(.05,.11,.11),'R_LowerArm',(.08+i*.15,0,.02),m=M(Bc),bev=0)
    pt('cyl',(.02,.02,.36),'R_LowerArm',(.9,0,-.17),m=M('#b8bcc4'))
    pt('tor',(.06,.018),'R_LowerArm',(.9,0,-.37),rot=(90,0,0),m=M('#b8bcc4'))
    pt('box',(.12,.12,.16),'R_UpperArm',(.05,0,.02),m=M(Bc),bev=.02)
    pt('box',(.4,.22,.28),'L_LowerArm',(-L*.5,0,0),m=M(O),bev=.02)
    for i in range(4):pt('box',(.03,.23,.26),'L_LowerArm',(-L*.5-.15+i*.1,0,0),m=M('#b84a10'),bev=0)
    pt('box',(.3,.18,.18),'C_UpperChest',(0,-.18,.05),m=M(Bc),bev=.02)
    pt('box',(.4,.2,.3),'C_UpperChest',(0,.03,0),m=M(A),bev=.03)
    for i in range(4):pt('box',(.06,.205,.04),'C_UpperChest',(-.15+i*.1,.03,-.12),rot=(0,35,0),m=M(Bc),bev=0)
    pt('hemi',(.22,.22,.15),'L_UpperArm',(-.03,0,.03),rot=(0,-25,0),m=M(A))
    boots(A,Bc,C);belt(Bc,C)
    return ['C_Head','L_Hand','R_Hand']
def d_neon():
    A,Bc,P1,C='#c82a9a','#2a0a3a','#ff5ad8','#7fe8ff'
    pt('cyl',(.05,.05,.12),'C_Head',(0,0,.03),m=M(Bc),bone='C_Neck')
    pt('box',(.48,.08,.3),'C_Head',(0,0,.17),m=M(Bc),bone='C_Neck',bev=.02)
    pt('box',(.43,.085,.25),'C_Head',(0,0,.17),m=G(P1),bone='C_Neck',bev=0)
    for sx in(-1,1):pt('box',(.08,.02,.05),'C_Head',(sx*.09,.05,.18),m=M('#14061e'),bone='C_Neck',bev=0)
    pt('box',(.12,.02,.02),'C_Head',(0,.05,.1),m=M('#14061e'),bone='C_Neck',bev=0)
    for sx in(-1,1):pt('cone',(.04,.04,.14),'C_Head',(sx*.2,0,.36),rot=(0,sx*25,0),m=G(C),bone='C_Neck')
    for S_,sx in SIDES:
        L=arm_len(S_)
        for i,f in enumerate((.25,.6,.95)):pt('tor',(.055,.014),S_+'_LowerArm',(sx*L*f,0,0),rot=(0,90,0),m=G(C if i%2 else P1))
        pt('tor',(.06,.014),S_+'_UpperArm',(sx*.12,0,0),rot=(0,90,0),m=G(P1))
        pt('sph',(.11,.11,.11),S_+'_LowerArm',(sx*(L+.04),0,0),m=G(C),seg=14)
    for i,(x,c) in enumerate(((-.12,P1),(-.06,C),(0,'#ffe14d'),(.06,P1),(.12,C))):
        pt('box',(.04,.015,.75),'C_UpperChest',(x,-.12,-.35),rot=(8,0,0),m=G(c),bev=0)
    pt('box',(.34,.16,.22),'C_UpperChest',(0,.03,0),m=M(A),bev=.03)
    pt('tor',(.13,.02),'C_UpperChest',(0,.11,0),rot=(90,0,0),m=G(C))
    boots(A,Bc,C);belt(Bc,P1)
    return ['C_Head','L_Hand','R_Hand']
def d_liner():
    A,GN,C='#e8ecf4','#3a8a3a','#fff6c0'
    pt('box',(.52,.44,.62),'C_Chest',(0,.03,.05),m=M(A),bev=.1)
    pt('box',(.44,.03,.2),'C_Chest',(0,.25,.24),m=M('#1a2430'),bev=.02)
    eyes2('C_Chest',C,.27,.24,x=.1,r=.06)
    pt('box',(.53,.45,.06),'C_Chest',(0,.03,-.04),m=M(GN),bev=0)
    for sx in(-1,1):pt('sph',(.08,.04,.08),'C_Chest',(sx*.17,.25,-.12),m=G(C),seg=12)
    pt('box',(.2,.03,.06),'C_Chest',(0,.255,.38),m=G('#ff9a3a'),bev=0)
    pt('box',(.4,.15,.06),'C_Chest',(0,.2,-.28),rot=(-30,0,0),m=M('#5a606c'))
    for sx in(-1,1):pt('box',(.025,.025,.3),'C_Chest',(sx*.08,0,.48),rot=(0,sx*30,0),m=M('#5a606c'))
    pt('box',(.36,.04,.025),'C_Chest',(0,0,.61),m=M('#5a606c'))
    for S_,sx in SIDES:
        pt('cyl',(.2,.2,.05),S_+'_Foot',(sx*.08,.04,0),rot=(0,90,0),m=M('#2a2a30'))
        pt('tor',(.1,.015),S_+'_Foot',(sx*.11,.04,0),rot=(0,90,0),m=G(C))
        pt('cyl',(.09,.09,.09),S_+'_Hand',(sx*.04,0,0),rot=(0,90,0),m=M('#5a606c'))
        pt('hemi',(.2,.2,.14),S_+'_UpperArm',(sx*.03,0,.03),rot=(0,sx*25,0),m=M(GN))
    boots(A,GN,C);belt(GN,C)
    return ['C_Head']
def d_wave():
    A,Bc,C,W='#2a9ad8','#0a3a5a','#bff4ff','#e8f6ff'
    pt('sph',(.28,.3,.3),'C_Head',(0,0,.12),m=M(A),bone='C_Neck',seg=24)
    pt('sph',(.22,.1,.12),'C_Head',(0,.12,.1),m=M('#06162a'),bone='C_Neck',seg=18)
    eyes2('C_Head',C,.17,.1,bone='C_Neck')
    pt('cone',(.06,.42,.38),'C_Head',(0,-.08,.32),rot=(-35,0,0),m=M(A),bone='C_Neck')
    for i in range(3):pt('sph',(.07,.07,.07),'C_Head',(0,.06-i*.05,.42-i*.03),m=M(W),bone='C_Neck',seg=10)
    for sx in(-1,1):pt('cone',(.04,.18,.2),'C_Head',(sx*.15,-.02,.15),rot=(0,sx*70,0),m=M(W),bone='C_Neck')
    pt('cyl',(.025,.025,.95),'R_Hand',(0,.25,0),rot=(90,0,0),m=M('#a8c8d8'))
    pt('box',(.2,.03,.03),'R_Hand',(0,.7,0),m=M('#a8c8d8'),bev=0)
    for dx in(-.08,0,.08):pt('cone',(.05,.05,.16),'R_Hand',(dx,.8,0),rot=(-90,0,0),m=G(C))
    pt('sph',(.06,.7,.26),'L_LowerArm',(-.18,0,0),m=M(W),seg=20)
    pt('box',(.065,.55,.03),'L_LowerArm',(-.18,0,0),m=G(C),bev=0)
    for S_,sx in SIDES:pt('cone',(.04,.3,.26),S_+'_Foot',(0,-.12,.05),rot=(25,0,0),m=M(A))
    pt('box',(.32,.15,.2),'C_UpperChest',(0,.02,0),m=M(A),bev=.03)
    boots(A,Bc,C);belt(Bc,C)
    return ['C_Head']
def d_shade(sp=False):
    A,Bc,C=('#5a2a7a','#1a0a28','#ff9aff') if sp else ('#3a2a5a','#120a20','#b98cff')
    pt('sph',(.26,.28,.3),'C_Head',(0,0,.12),m=M(Bc),bone='C_Neck',seg=24)
    pt('tor',(.135,.025),'C_Head',(0,0,.17),m=M(A),bone='C_Neck')
    pt('box',(.2,.03,.035),'C_Head',(0,.13,.14),m=G(C),bone='C_Neck',bev=0)
    for sx in(-1,1):pt('box',(.04,.4,.02),'C_Head',(sx*.04,-.3,.12),rot=(-20,sx*8,0),m=M(A),bone='C_Neck',bev=0)
    for i in range(3 if not sp else 4):pt('box',(.12,.5,.02),'C_Neck',(0,-.18-i*.42,-.08-i*.12),rot=(-12-i*6,0,0),m=M(A),bev=0)
    for S_,sx in SIDES:
        pt('cone',(.05,.025,.4),S_+'_Hand',(0,.22,0),rot=(-90,0,0),m=G(C))
        pt('cone',(.14,.14,.2),S_+'_UpperArm',(sx*.04,0,.06),rot=(0,sx*60,0),m=M(Bc))
    pt('tor',(.07,.012),'C_Hips',(.12,.15,.06),rot=(90,0,0),m=G(C))
    pt('tor',(.42,.015),'C_Hips',(0,0,-.1),m=G(C))
    if sp:pt('tor',(.3,.012),'C_Hips',(0,0,.25),rot=(10,0,0),m=G(C))
    boots(A,Bc,C);belt(Bc,C)
    return ['C_Head']
def d_hanabi():
    R,W,Y,K='#d83a3a','#f4e8d8','#ffd24a','#2a0a12'
    pt('sph',(.32,.32,.32),'C_Head',(0,0,.14),m=M(R),bone='C_Neck',seg=26)
    pt('tor',(.163,.018),'C_Head',(0,0,.14),rot=(0,90,0),m=M(W),bone='C_Neck')
    pt('tor',(.163,.018),'C_Head',(0,0,.14),rot=(90,0,0),m=M(W),bone='C_Neck')
    pt('sph',(.2,.08,.1),'C_Head',(0,.13,.13),m=M('#14060a'),bone='C_Neck',seg=16)
    eyes2('C_Head',Y,.17,.13,bone='C_Neck')
    pt('cyl',(.03,.03,.14),'C_Head',(0,-.02,.35),rot=(-15,0,0),m=M(K),bone='C_Neck')
    pt('sph',(.07,.07,.07),'C_Head',(0,-.04,.43),m=G('#ff8a3a'),bone='C_Neck',seg=10)
    for S_,sx in SIDES:
        for j,dx in enumerate((.0,.1)):
            pt('cyl',(.1,.1,.36),'C_UpperChest',(sx*(.14+dx),-.1,.2),rot=(-15,sx*12,0),m=M(R if j==0 else W))
            pt('tor',(.05,.014),'C_UpperChest',(sx*(.14+dx)+sx*.04,-.15,.37),rot=(-15,sx*12,0),m=G(Y))
        L=arm_len(S_)
        pt('cyl',(.13,.13,L*.95),S_+'_LowerArm',(sx*L*.5,0,0),rot=(0,90,0),m=M(R))
        pt('tor',(.065,.016),S_+'_LowerArm',(sx*(L+.02),0,0),rot=(0,90,0),m=G(Y))
    pt('box',(.38,.22,.34),'C_UpperChest',(0,.02,-.04),m=M(R),bev=.03)
    pt('box',(.04,.23,.34),'C_UpperChest',(0,.02,-.04),m=M(W),bev=0)
    boots(R,K,Y);belt(K,Y)
    return ['C_Head','L_Hand','R_Hand']
def d_bridge():
    W,N,Gc='#dfe4ee','#2a3a5a','#7dff9a'
    pt('box',(.24,.24,.26),'C_Head',(0,0,.12),m=M(N),bone='C_Neck',bev=.03)
    pt('box',(.22,.04,.06),'C_Head',(0,.12,.13),m=G(Gc),bone='C_Neck',bev=0)
    for sx in(-1,1):pt('cyl',(.02,.02,.16),'C_Head',(sx*.08,0,.32),m=M(W),bone='C_Neck')
    for S_,sx in SIDES:
        pt('box',(.08,.08,.6),'C_UpperChest',(sx*.2,-.04,.3),m=M(W))
        pt('box',(.09,.09,.06),'C_UpperChest',(sx*.2,-.04,.42),m=M(N),bev=0)
        pt('sph',(.06,.06,.06),'C_UpperChest',(sx*.2,-.04,.62),m=G(Gc),seg=10)
        L=arm_len(S_)
        pt('box',(L*.8,.2,.2),S_+'_LowerArm',(sx*L*.5,0,0),m=M(W),bev=.03)
        pt('box',(.27,.27,.27),S_+'_LowerArm',(sx*(L+.08),0,0),m=M(N),bev=.04)
        pt('box',(.04,.205,.205),S_+'_LowerArm',(sx*L*.5,0,0),m=G(Gc),bev=0)
    pt('box',(.5,.06,.06),'C_UpperChest',(0,-.04,.5),m=M(W))
    for i,c in enumerate(('#ff5ad8','#5ad8ff',Gc,'#ffe14d')):pt('box',(.42,.01,.025),'C_UpperChest',(0,.13,.1-i*.06),m=G(c),bev=0)
    pt('box',(.46,.24,.34),'C_UpperChest',(0,.0,-.02),m=M(N),bev=.03)
    boots(W,N,Gc);belt(N,Gc)
    return ['C_Head','L_Hand','R_Hand']
def d_blackout(sp=False):
    A,K,C=('#2a0a12','#06060a','#ffd24a') if sp else ('#1a1a22','#06060a','#ff3b5c')
    pt('sph',(.3,.3,.34),'C_Head',(0,0,.2),m=M('#2a2a34'),bone='C_Neck',seg=26)
    pt('tor',(.05,.012),'C_Head',(0,0,.22),rot=(90,0,0),m=G(C),bone='C_Neck')
    eyes2('C_Head',C,.145,.18,x=.07,r=.055,bone='C_Neck')
    pt('cyl',(.18,.18,.12),'C_Head',(0,0,.0),m=M('#8a8a96'),bone='C_Neck')
    for z in(-.03,0,.03):pt('tor',(.092,.012),'C_Head',(0,0,z),m=M('#5a5a66'),bone='C_Neck')
    if sp:pt('tor',(.2,.02),'C_Head',(0,0,.44),m=G(C),bone='C_Neck')
    segs=[(0,-.14,.0),(0,-.3,-.18),(0,-.46,-.4),(0,-.6,-.62)]
    for i,o in enumerate(segs):pt('sph',(.07,.07,.07),'C_Hips',o,m=M(K),seg=10)
    for i in range(3):
        a=Vector(segs[i]);b=Vector(segs[i+1]);c=(a+b)/2;d=b-a
        rx=math.degrees(math.atan2(-d.y,d.z)) if True else 0
        pt('cyl',(.045,.045,d.length),'C_Hips',tuple(c),rot=(rx,0,0),m=M(K))
    pt('box',(.12,.08,.1),'C_Hips',(0,-.66,-.72),m=M(A),bev=.02)
    for sx in(-1,1):pt('box',(.02,.02,.08),'C_Hips',(sx*.03,-.66,-.8),m=G(C),bev=0)
    for S_,sx in SIDES:
        pt('cone',(.14,.14,.3),S_+'_UpperArm',(sx*.05,0,.08),rot=(0,sx*55,0),m=M(K))
        for j,dz in enumerate((-.03,0,.03)):pt('cone',(.035,.035,.16),S_+'_Hand',(sx*.12,.03,dz),rot=(0,sx*90,0),m=G(C))
        pt('hemi',(.2,.2,.14),S_+'_UpperArm',(sx*.03,0,.03),rot=(0,sx*25,0),m=M(A))
    if sp:
        for sx in(-1,1):pt('cone',(.35,.06,.7),'C_UpperChest',(sx*.3,-.18,.15),rot=(0,sx*-40,0),m=G(C))
    pt('box',(.4,.22,.32),'C_UpperChest',(0,.02,-.02),m=M(A),bev=.03)
    pt('tor',(.1,.02),'C_UpperChest',(0,.13,0),rot=(90,0,0),m=G(C))
    boots(A,K,C);belt(K,C)
    return ['C_Head']
DES={'dam':d_dam,'crane':d_crane,'neon':d_neon,'liner':d_liner,'wave':d_wave,'shade':d_shade,'shadesp':lambda:d_shade(True),'hanabi':d_hanabi,'bamboo':d_bridge,'blackout':d_blackout,'blackoutsp':lambda:d_blackout(True)}
def nbuild(k,prev=True,exp=True):
    vr=setupv(GEN[k]);hide=DES[k]()
    # hide human head/hands in preview
    for b in hide:
        pb=vr.pose.bones.get(bj(b))
        if pb:pb.scale=(.001,.001,.001)
    if prev:
        vr.data.pose_position='POSE';setup_view();cam=bpy.data.objects['PCam'];cam.location=(-1.6,3.6,1.6);d=Vector((0,0,1.15))-cam.location;cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
        S().render.filepath=D+'pn_'+k+'.png';bpy.ops.render.render(write_still=True)
    for b in hide:
        pb=vr.pose.bones.get(bj(b))
        if pb:pb.scale=(1,1,1)
    vr.data.pose_position='REST'
    if exp:
        bpy.ops.object.select_all(action='DESELECT');vr.select_set(True)
        for o in vr.children_recursive:
            if o.name.startswith('NX_'):o.select_set(True)
        bpy.context.view_layer.objects.active=vr
        bpy.ops.export_scene.gltf(filepath=D+'pn_'+k+'.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_animations=False,export_skins=True,export_apply=True)
    return hide
def nall(ks=None):
    out={}
    for k in (ks or list(DES)):
        try:out[k]=nbuild(k)
        except Exception as e:
            import traceback;out[k]=traceback.format_exc()[-700:]
    return out
