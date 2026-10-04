import bpy
from mathutils import Vector
def shots(scn,prefix,center_z=0.5,scale=1.4,views=(('f',(0,3,0),(0,-1,0)),('s',(3,0,0),(-1,0,0)))):
    sc=bpy.data.scenes[scn];bpy.context.window.scene=sc
    cam=bpy.data.objects.get('RCam') or bpy.data.objects.new('RCam',bpy.data.cameras.new('RCam'))
    if cam.name not in sc.objects:sc.collection.objects.link(cam)
    sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=scale
    sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='FLAT';sc.display.shading.color_type='TEXTURE'
    sc.render.resolution_x=500;sc.render.resolution_y=500
    outs=[]
    for nm,loc,d in views:
        cam.location=(loc[0],loc[1],center_z);cam.rotation_euler=Vector(d).to_track_quat('-Z','Y').to_euler()
        f=r'C:\Users\LoZy\Downloads\nl_kk\%s_%s.png'%(prefix,nm);sc.render.filepath=f;bpy.ops.render.render(write_still=True);outs.append(f)
    return outs
