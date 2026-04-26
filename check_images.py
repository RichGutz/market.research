import base64
from PIL import Image
import io

def check_image(path):
    try:
        with Image.open(path) as img:
            print(f"Image: {path}")
            print(f"  Format: {img.format}")
            print(f"  Mode: {img.mode}")
            print(f"  Size: {img.size}")
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                print("  Has Transparency: Yes")
            else:
                print("  Has Transparency: No")
    except Exception as e:
        print(f"Error checking {path}: {e}")

images = ["logo_cyan_pure.png", "logo_emerald_pure.png", "logo_pink_pure.png"]
for img_path in images:
    check_image(img_path)

# Generate high quality base64 for Emerald if it's the best
try:
    with open("logo_emerald_pure.png", "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode('utf-8')
        with open("clean_silhouette.txt", "w") as out:
            out.write(f"data:image/png;base64,{encoded}")
    print("\nGenerated clean_silhouette.txt from logo_emerald_pure.png")
except Exception as e:
    print(f"Error generating base64: {e}")
