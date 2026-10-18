# 無料素材（Kenney CC0 / Japanese Street / Majadroid CC0）から町用ライブラリ town.glb を作る
import bpy,os,sys,mathutils
A='/tmp/claude-0/assets/'
K=lambda kit,n:A+'kenney_city-kit-%s/Models/GLB format/%s.glb'%(kit,n)
items=[]
for n in 'acehiklpqrs':items.append(('sub_'+n,K('suburban_2.0','building-type-'+n),None))
for n in ['fence-low','fence','planter','driveway-short','path-short','tree-large','tree-small']:items.append(('sub_'+n,K('suburban_2.0',n),None))
for n in ['building-a','building-b','building-c','building-d','building-e','building-g','building-i','building-j','building-k','building-l','building-m','building-n','building-skyscraper-a','building-skyscraper-b','detail-awning','detail-awning-wide','detail-overhang','low-detail-building-a','low-detail-building-c','low-detail-building-k','low-detail-building-wide-a']:items.append(('com_'+n,K('commercial_2.1',n),None))
for n in ['building-h','building-i','building-j','building-k','building-s','building-p','chimney-small','chimney-medium','detail-tank','detail-tank-large','shipping-container-a','shipping-container-b','shipping-container-c','water-tower']:items.append(('ind_'+n,K('industrial_2.0',n),None))
for n in ['road-straight','road-crossroad','road-intersection','road-crossing','road-side','road-end','road-bend-sidewalk','tile-low','light-square','light-curved','traffic-light','road-sign-street','construction-cone','construction-barrier','dumpster','electricity-pole','electricity-wires']:items.append(('road_'+n,K('roads_2.2',n),None))
J=A+'jpstreet/Japanese Street/'
for n in ['House1','House2','House3','Wall','Electric Pole','Electric Pole Cable']:items.append(('jp_'+n.replace(' ','_'),J+n+'/'+n+'.fbx',n))
items.append(('jb_corner',A+'jb04/out/Assets/INDIEPLAY/JapaneseBuildings04/Meshes/JPBM06Base.obj',None))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
done=[]
for key,f,only in items:
    before=set(bpy.data.objects)
    try:
        if f.endswith('.fbx'):bpy.ops.import_scene.fbx(filepath=f)
        elif f.endswith('.obj'):bpy.ops.wm.obj_import(filepath=f)
        else:bpy.ops.import_scene.gltf(filepath=f)
    except Exception as e:print('ERR',key,e);continue
    new=[o for o in bpy.data.objects if o not in before]
    if only:
        for o in list(new):
            if o.type=='MESH' and o.name.split('.')[0]!=only:bpy.data.objects.remove(o);new.remove(o)
        # 素材の画像テクスチャ
        img=bpy.data.images.load(os.path.dirname(f)+'/'+only+'.png')
        for o in new:
            if o.type!='MESH':continue
            m=bpy.data.materials.new(key+'_m');m.use_nodes=True;nt=m.node_tree;bs=nt.nodes['Principled BSDF'];tx=nt.nodes.new('ShaderNodeTexImage');tx.image=img;nt.links.new(tx.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.85
            o.data.materials.clear();o.data.materials.append(m)
    meshes=[o for o in new if o.type=='MESH']
    if only:
        tgt=1500 if 'Pole' in only else (300 if only=='Wall' else 7000)
        for o in meshes:
            nf=len(o.data.polygons);bpy.context.view_layer.objects.active=o
            if nf>tgt:
                md=o.modifiers.new('d','DECIMATE');md.ratio=tgt/nf;bpy.ops.object.modifier_apply(modifier='d')
            print('JPF',key,nf,'->',len(o.data.polygons))
    if not meshes:print('NOMESH',key);continue
    bpy.context.view_layer.update()
    pts=[o.matrix_world@mathutils.Vector(c) for o in meshes for c in o.bound_box]
    mn=mathutils.Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)));mx=mathutils.Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
    cen=mathutils.Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z))
    root=bpy.data.objects.new(key,None);sc.collection.objects.link(root)
    for o in new:
        if o.parent is None or o.parent not in new:
            mw=o.matrix_world.copy();o.parent=root;o.matrix_world=mathutils.Matrix.Translation(-cen)@mw
    done.append((key,[round(v,2) for v in (mx-mn)]))
for d in done:print('LIB',d)
for im in bpy.data.images:
    if im.size[0]>512:im.scale(512,int(512*im.size[1]/im.size[0]))
bpy.ops.export_scene.gltf(filepath=A+'town.glb',export_format='GLB',export_image_format='WEBP',export_animations=False)
print('OUT',os.path.getsize(A+'town.glb'))
