# render_blend_scene.py
import blenderproc as bproc
import numpy as np
import os, math
import bpy  # available inside BlenderProc

BLEND_PATH = "scene.blend"
OUTPUT_DIR = "output"

bproc.init()

if not os.path.exists(BLEND_PATH):
    raise FileNotFoundError(BLEND_PATH)

objs = bproc.loader.load_blend(BLEND_PATH)

# Light (optional)
sun = bproc.types.Light()
sun.set_type("SUN")
sun.set_energy(3.0)
sun.set_rotation_euler([-np.pi/4, 0, np.pi/4])

# Find Blender cameras
blend_cams = [ob for ob in bpy.data.objects if ob.type == 'CAMERA']

if blend_cams:
    scene = bpy.context.scene
    res_x, res_y = scene.render.resolution_x, scene.render.resolution_y

    for ob in blend_cams:
        mw = np.array(ob.matrix_world)            # camera-to-world (4x4)
        bproc.camera.set_intrinsics_from_blender_params(50, 1920, 1080)
        bproc.camera.add_camera_pose(mw)

else:
    # Fallback: add a default camera
    cam_pose = bproc.math.build_transformation_mat([0, -5, 3], [1.1, 0.0, 0.0])
    bproc.camera.add_camera_pose(cam_pose)
    bproc.camera.set_intrinsics_from_blender_params(50, 1920, 1080)

data = bproc.renderer.render()
os.makedirs(OUTPUT_DIR, exist_ok=True)
bproc.writer.write_hdf5(OUTPUT_DIR, data)
print(f"Done → {OUTPUT_DIR}")
