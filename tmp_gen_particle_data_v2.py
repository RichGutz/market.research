import numpy as np
from PIL import Image
import json

def get_pts(path, count=10000): # Reduced to 10k for stability
    img = Image.open(path).convert("RGBA")
    img = img.resize((150, 150), Image.Resampling.LANCZOS)
    data = np.array(img)
    alpha = data[:, :, 3]
    
    y, x = np.where(alpha > 128)
    # Normalize
    pts = np.stack([(x - 75) / 75.0, (75 - y) / 75.0, np.zeros_like(x)], axis=-1).astype(np.float32)
    
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
    f.write("window.PARTICLE_DATA = " + json.dumps(result) + ";")

print("Optimized particle data (10k) generated in particle_data.js")
