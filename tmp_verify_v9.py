from PIL import Image
import numpy as np
import os

def check_file(path):
    if not os.path.exists(path):
        print(f"File {path} does not exist!")
        return
    
    img = Image.open(path)
    arr = np.array(img)
    
    print(f"--- Ficha Técnica: {path} ---")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")
    print(f"File Size: {os.path.getsize(path)} bytes")
    
    # Check if image is constant
    if np.all(arr == arr[0,0]):
        print("ALERTA: La imagen es un bloque sólido de un solo color!")
    else:
        # Count non-zero alpha
        if img.mode == "RGBA":
            alpha = arr[..., 3]
            opaque_count = np.count_nonzero(alpha > 0)
            print(f"Píxeles no transparentes: {opaque_count} / {alpha.size}")
            
            # Check for dots (small isolated alpha pixels)
            # (Just a simple heuristic)
        
    # Check RGB channels
    print(f"Mean RGB: {np.mean(arr[..., :3], axis=(0,1))}")

check_file("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v9.png")
check_file("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v9.png")
check_file("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v9.png")
