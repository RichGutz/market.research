import base64
from PIL import Image, ImageFilter
import io
import numpy as np
from scipy import ndimage

def create_final_hd_v10(color_hex, output_path):
    # 1. Cargar la Rosetta y extraer la forma de los canales RGB
    base = Image.open("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_from_html.png").convert("RGB")
    arr = np.array(base)
    
    # La máscara es cualquier cosa que no sea negro (umbral bajo para capturar anti-aliasing)
    mask = np.any(arr > 2, axis=-1)
    
    # 2. Rellenar huecos internos (los puntos que el usuario odia)
    mask = ndimage.binary_fill_holes(mask)
    
    # 3. Crear el canal Alpha (con un poco de suavizado para bordes perfectos)
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=0.2))
    
    # 4. Construir la imagen RGBA
    width, height = base.size
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    
    # Fondo negro sólido (importantísimo para compatibilidad con luminancia)
    final_arr = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Aplicar color solo en la silueta
    mask_arr = np.array(mask_img)
    mask_norm = mask_arr / 255.0
    
    final_arr[..., 0] = (color_rgb[0] * mask_norm).astype(np.uint8)
    final_arr[..., 1] = (color_rgb[1] * mask_norm).astype(np.uint8)
    final_arr[..., 2] = (color_rgb[2] * mask_norm).astype(np.uint8)
    final_arr[..., 3] = mask_arr # Canal Alpha
    
    result = Image.fromarray(final_arr, mode='RGBA')
    
    # Sharpen para la nitidez "Apple"
    result = result.filter(ImageFilter.SHARPEN)
    
    result.save(output_path)
    return output_path

# Generar v10
create_final_hd_v10("#00e3fd", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v10.png")
create_final_hd_v10("#ed1ad9", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v10.png")
create_final_hd_v10("#b0ff00", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v10.png")
