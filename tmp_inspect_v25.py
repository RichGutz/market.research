import base64
from PIL import Image
import io
import numpy as np

def inspect_b64_metadata(html_path, index):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extraer el Base64 nro index del array IMG_DATA
    import re
    # Buscamos el contenido entre comillas dentro de IMG_DATA[index]
    matches = re.findall(r"'data:image/png;base64,(.*?)'", content)
    if index >= len(matches):
        print(f"Index {index} out of range (max {len(matches)-1})")
        return
    
    b64_data = matches[index]
    img_data = base64.b64decode(b64_data)
    img = Image.open(io.BytesIO(img_data))
    
    print(f"--- Inspección V25 IMG_DATA[{index}] ---")
    print(f"Modo: {img.mode}")
    print(f"Tamaño: {img.size}")
    
    if img.mode == "RGBA":
        alpha = np.array(img.split()[3])
        print(f"Alpha Mean: {np.mean(alpha)}")
        print(f"Alpha Max: {np.max(alpha)}")
        print(f"Alpha Min: {np.min(alpha)}")
    else:
        print("No tiene canal Alpha.")
    
    # Guardar como referencia pura
    img.save(f"c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/inspect_v25_{index}.png")

# Inspeccionar el Cyan (0) y el Pink (1) de la V25 original
inspect_b64_metadata("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V25.html", 0)
inspect_b64_metadata("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V25.html", 1)
