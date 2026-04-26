from PIL import Image
import numpy as np

def inspect_pixels(path):
    img = Image.open(path)
    arr = np.array(img)
    
    # Tomar una muestra del centro (asumiendo que ahí está la silueta)
    h, w = arr.shape[:2]
    sample = arr[h//2-5:h//2+5, w//2-5:w//2+5]
    
    print(f"--- Píxeles en {path} ---")
    print(f"Modo: {img.mode}")
    print(f"Esquina (0,0): {arr[0,0]}")
    print(f"Centro (320,320): {arr[h//2, w//2]}")
    
    # ¿Hay píxeles negros puros?
    black_count = np.count_nonzero(np.all(arr == [0, 0, 0], axis=-1))
    print(f"Píxeles negros: {black_count} / {h*w}")

inspect_pixels("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/inspect_v25_0.png")
inspect_pixels("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/inspect_v25_1.png")
