# quickstart.py
import blenderproc as bproc
import numpy as np
import os

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------
# Path to your Unity-exported scene (.glb)
SCENE_PATH = "scene.glb"
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

# -------------------------------------------------------
# Set up camera
# -------------------------------------------------------
# Camera at (x=0, y=-8, z=4) looking at the origin
location = np.array([0.0, -15.0, 4.0])
rotation = bproc.math.build_transformation_mat(location, [np.radians(70), 0, 0])

bproc.camera.add_camera_pose(rotation)

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
