import bpy,json
from mathutils import Vector
D=r'C:\Users\LoZy\Downloads\nl_kk\\'
def hyview(k):
    if 'NL_HY' not in bpy.data.scenes:bpy.data.scenes.new('NL_HY')
    sc=bpy.data.scenes['NL_HY'];bpy.context.window.scene=sc
    for o in list(sc.objects):bpy.data.objects.remove(o,do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=D+'hy_%s.glb'%k)
    ms=[o for o in sc.objects if o.type=='MESH']
    vs=[o.matrix_world@Vector(b) for o in ms for b in o.bound_box]
    mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
    cam=bpy.data.objects.get('HYCam') or bpy.data.objects.new('HYCam',bpy.data.cameras.new('HYCam'))
    if cam.name not in sc.objects:sc.collection.objects.link(cam)
    sc.camera=cam;cam.data.type='ORTHO'
    S=max(mx[2]-mn[2],mx[0]-mn[0],mx[1]-mn[1])*1.08;cz=(mn[2]+mx[2])/2
    cam.data.ortho_scale=S
    sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='FLAT';sc.display.shading.color_type='TEXTURE'
    sc.render.resolution_x=600;sc.render.resolution_y=600
    for nm,loc,d in(('of',(0,-5,cz),(0,1,0)),('os',(-5,0,cz),(1,0,0))):
        cam.location=loc;cam.rotation_euler=Vector(d).to_track_quat('-Z','Y').to_euler()
        sc.render.filepath=D+'hy_%s_%s.png'%(k,nm);bpy.ops.render.render(write_still=True)
    meta={'S':S,'cz':cz,'mn':mn,'mx':mx}
    open(D+'hy_%s_meta.json'%k,'w').write(json.dumps(meta));return meta
