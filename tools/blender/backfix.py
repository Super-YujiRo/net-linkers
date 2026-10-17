import bpy,sys,os,mathutils
src,dst,BIx=sys.argv[-3],sys.argv[-2],sys.argv[-1]
os.environ['BACKIMG']=BIx
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
arm=[o for o in bpy.data.objects if o.type=='ARMATURE'][0];me=[o for o in bpy.data.objects if o.type=='MESH']
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
    # 背面画像の頭部分を切り出し（zneck〜zmax）
    hx0=hx1=None
    uvl=m.data.uv_layers.active.data;N=np.array([tuple((mw.to_3x3()@p.normal).normalized()) for p in m.data.polygons])
    sel=[]
    HV=V[V[:,2]>zneck];ymid=(HV[:,1].min()+HV[:,1].max())/2;yd=HV[:,1].max()-HV[:,1].min()
    BK=float(os.environ.get('BACKCUT','0.12'))
    for p in m.data.polygons:
        P=V[list(p.vertices)]
        if P[:,2].min()<zneck-0.01*(zmax-zmin):continue
        if (BS*(P[:,1]-ymid)).min()<BK*yd:continue   # 頭の後ろ側（位置で判定：法線は裏返りがあるので使わない）
        sel.append(p)
    HP=V[sorted({v for p in sel for v in p.vertices})]
    u,v=proj(HP);u0,u1,v0,v1=u.min(),u.max(),v.min(),v.max();pad=2
    u0-=pad;u1+=pad;v0-=pad;v1+=pad
    crop=sp[int(max(0,v0)):int(min(sh,v1)),int(max(0,u0)):int(min(sw,u1))]
    import numpy as _np
    from PIL import Image as _I
    ci=_I.fromarray((_np.clip(crop,0,1)*255).astype(_np.uint8)).resize((tw,th),_I.LANCZOS)
    R=_np.asarray(ci).astype(_np.float32)/255
    NT=_np.concatenate([T,R],axis=1)  # 横に2倍
    for l in uvl:l.uv=(l.uv[0]*0.5,l.uv[1])
    for p in sel:
        for li in p.loop_indices:
            q=V[m.data.loops[li].vertex_index][None,:];uu,vv=proj(q)
            uvl[li].uv=(0.5+0.5*float((uu[0]-u0)/(u1-u0)),float((vv[0]-v0)/(v1-v0)))
    cnt=len(sel)
    fp=os.path.join(os.path.dirname(os.path.abspath(dst)),'_backfixed.png')
    nim=bpy.data.images.new('basecolor_fixed',tw*2,th,alpha=True);nim.pixels.foreach_set(NT.ravel());nim.filepath_raw=fp;nim.file_format='PNG';nim.save()
    nim2=bpy.data.images.load(fp);nim2.pack()
    for n in mat.node_tree.nodes:
        if n.type=='TEX_IMAGE' and n.image==tex:n.image=nim2
    print('backfix polys',cnt,'zneck',round(zneck,3))

bpy.ops.export_scene.gltf(filepath=dst,export_format='GLB',export_animations=False,export_skins=True,export_image_format='WEBP')
print('OUT',os.path.getsize(dst))
