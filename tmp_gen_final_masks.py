import base64
from PIL import Image
import io

def get_optimized_b64(path, size=(200, 200)):
    img = Image.open(path).convert("RGBA")
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Grayscale mask for sampling
    mask = img.split()[-1] # Alpha channel
    
    buffered = io.BytesIO()
    # Save as highly compressed PNG
    mask.save(buffered, format="PNG", optimize=True)
    return base64.b64encode(buffered.getvalue()).decode()

files = {
    'cyan': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_cyan.png',
    'pink': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_pink.png',
    'emerald': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_emerald.png'
}

with open('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/final_masks.txt', 'w') as f:
    for name, path in files.items():
        b64 = get_optimized_b64(path)
        f.write(f"const MASK_{name.upper()} = 'data:image/png;base64,{b64}';\n")

print("High-fidelity masks generated in final_masks.txt")
