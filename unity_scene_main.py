# quickstart.py
import blenderproc as bproc
import numpy as np
import json, os

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
# Path to your Unity-exported scene (.glb)
SCENE_PATH = "scene.glb"
CAM   = "camera_positions.txt"    # exported by the Unity script
OUTPUT_DIR = "output"

# -------------------------------------------------------
# Initialization
# -------------------------------------------------------
bproc.init()

# -------------------------------------------------------
# Load exported GLB scene
# -------------------------------------------------------
if not os.path.exists(SCENE_PATH):
    raise FileNotFoundError(f"Scene file not found: {SCENE_PATH}")

print(f"Loading scene from {SCENE_PATH}")
objects = bproc.loader.load_obj(SCENE_PATH)

print(f"Loaded {len(objects)} objects")

# -------------------------------------------------------
# Set up lighting
# -------------------------------------------------------
# Simple sun light from above
light = bproc.types.Light()
light.set_type("SUN")
light.set_location([5, 5, 10])
light.set_rotation_euler([-np.pi / 4, 0, np.pi / 4])
light.set_energy(5.0)

# Optional: add ambient point light for softer illumination
fill_light = bproc.types.Light()
fill_light.set_type("POINT")
fill_light.set_location([0, 0, 3])
fill_light.set_energy(200.0)


def u2b(v):  # Unity (x,y,z) -> Blender (x,z,y)
    return np.array([v[0], v[2], v[1]], dtype=float)

def nrm(v):
    v = np.asarray(v, dtype=float)
    return v / (np.linalg.norm(v) + 1e-8)

with open(CAM, "r", encoding="utf-8-sig") as f:
    for line in f:
        vals = [float(x) for x in line.split()]
        if len(vals) < 9:
            continue
        p_u = vals[0:3]
        f_u = vals[3:6]
        u_u = vals[6:9]

        # axis remap to Blender world
        p_b = u2b(p_u)
        f_b = nrm(u2b(f_u))
        u_b = nrm(u2b(u_u))

        # construct camera basis: camera looks along -Z in Blender
        z_cam = -f_b
        x_cam = nrm(np.cross(u_b, z_cam))
        y_cam = np.cross(z_cam, x_cam)

        R = np.column_stack([x_cam, y_cam, z_cam])  # 3x3
        T = np.eye(4)
        T[:3, :3] = R
        T[:3,  3] = p_b

        bproc.camera.add_camera_pose(T)



# -------------------------------------------------------
# Render the scene
# -------------------------------------------------------
data = bproc.renderer.render()

# -------------------------------------------------------
# Save results
# -------------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
bproc.writer.write_hdf5(OUTPUT_DIR, data)

print(f"Rendering complete. Results written to '{OUTPUT_DIR}'")
