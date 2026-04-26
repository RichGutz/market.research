import base64
from PIL import Image
import io
import numpy as np
from scipy import ndimage

def surgical_clean_v25(html_path, index, output_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    import re
    matches = re.findall(r"'data:image/png;base64,(.*?)'", content)
    b64_data = matches[index]
    img_data = base64.b64decode(b64_data)
    img = Image.open(io.BytesIO(img_data)).convert("RGB")
    arr = np.array(img)
    
    # 1. Identificar la silueta (luminancia > umbral bajo)
    gray = np.mean(arr, axis=-1)
    mask = (gray > 10).astype(bool)
    
    # 2. Encontrar los "huecos" (puntos internos)
    filled_mask = ndimage.binary_fill_holes(mask)
    holes = filled_mask ^ mask # Esto son solo los puntos internos
    
    # 3. Rellenar SOLO los huecos con el color predominante de la silueta
    # Extraer color predominante (mediana para evitar picos de ruido)
    silhouette_pixels = arr[mask]
    avg_color = np.median(silhouette_pixels, axis=0).astype(np.uint8)
    
    # Aplicar el parche
    arr[holes] = avg_color
    
    # 4. Asegurar fondo negro puro para luminancia
    arr[~filled_mask] = [0, 0, 0]
    
    # 5. Guardar como JPEG con calidad máxima (para replicar el comportamiento de V25)
    result = Image.fromarray(arr, mode='RGB')
    result.save(output_path, "JPEG", quality=100)
    return output_path

# Procesar los originales de V25
surgical_clean_v25("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V25.html", 0, "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_v25_surgical.jpg")
surgical_clean_v25("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V25.html", 1, "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_v25_surgical.jpg")
surgical_clean_v25("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V25.html", 2, "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_v25_surgical.jpg")
