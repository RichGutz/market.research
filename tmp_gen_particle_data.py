import numpy as np
from PIL import Image
import json

def get_pts(path, count=30000):
    img = Image.open(path).convert("RGBA")
    # Resize to 200x200 for consistent sampling
    img = img.resize((200, 200), Image.Resampling.LANCZOS)
    data = np.array(img)
    alpha = data[:, :, 3]
    
    # Find active pixels
    y, x = np.where(alpha > 128)
    # Normalize to -1 to 1 range
    pts = np.stack([(x - 100) / 100.0, (100 - y) / 100.0, np.zeros_like(x)], axis=-1).astype(np.float32)
    
    # Resample to exact count
    if len(pts) > count:
        idx = np.random.choice(len(pts), count, replace=False)
        pts = pts[idx]
    elif len(pts) < count:
        extra = count - len(pts)
        idx = np.random.choice(len(pts), extra, replace=True)
        pts = np.concatenate([pts, pts[idx]], axis=0)
        
    return pts.flatten().tolist()

files = {
    'cyan': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_cyan.png',
    'pink': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_pink.png',
    'emerald': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_emerald.png'
}

result = {}
for name, path in files.items():
    result[name] = get_pts(path)

with open('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/particle_data.js', 'w') as f:
    f.write("const PARTICLE_DATA = " + json.dumps(result) + ";")

print("Particle data generated in particle_data.js")
