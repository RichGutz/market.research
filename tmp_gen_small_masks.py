import base64
from PIL import Image
import io

def get_optimized_b64(path, size=(128, 128)):
    img = Image.open(path).convert("RGBA")
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Convert to black and white mask for extreme compression
    mask = Image.new("L", img.size, 0)
    for x in range(img.width):
        for y in range(img.height):
            r, g, b, a = img.getpixel((x, y))
            if a > 128:
                mask.putpixel((x, y), 255)
    
    buffered = io.BytesIO()
    mask.save(buffered, format="PNG", optimize=True)
    return base64.b64encode(buffered.getvalue()).decode()

files = {
    'cyan': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_cyan.png',
    'pink': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_pink.png',
    'emerald': 'c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_emerald.png'
}

with open('c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/small_masks.txt', 'w') as f:
    for name, path in files.items():
        b64 = get_optimized_b64(path)
        f.write(f"{name.upper()}: data:image/png;base64,{b64}\n")

print("Small masks generated in small_masks.txt")
