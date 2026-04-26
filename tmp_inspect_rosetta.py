from PIL import Image
import numpy as np

def inspect_rosetta(path):
    img = Image.open(path).convert("RGB")
    arr = np.array(img)
    
    # Check if there's any non-black pixel
    non_black = np.any(arr != [0,0,0], axis=-1)
    non_black_count = np.count_nonzero(non_black)
    
    print(f"--- Inspección: {path} ---")
    print(f"Size: {img.size}")
    print(f"Píxeles no negros (Silueta potencial): {non_black_count} / {arr.shape[0]*arr.shape[1]}")
    
    # Calculate avg color of non-black pixels
    if non_black_count > 0:
        avg_color = np.mean(arr[non_black], axis=0)
        print(f"Color medio de la silueta: {avg_color}")
    else:
        print("ALERTA: La imagen es totalmente NEGRA!")

inspect_rosetta("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_from_html.png")
