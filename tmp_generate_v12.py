import base64
from PIL import Image, ImageFilter
import io
import numpy as np
from scipy import ndimage

def create_pure_gold_v12(color_hex, output_path):
    # 1. Cargar el Cyan Final validado (640x640)
    base = Image.open("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_final.png").convert("RGBA")
    
    # 2. Extraer Alpha
    alpha = np.array(base.split()[3])
    
    # 3. Limpieza de precisión (SÓLO rellenar huecos internos, nada de escalado)
    mask = (alpha > 128).astype(bool)
    mask = ndimage.binary_fill_holes(mask)
    
    # Re-obtener el canal Alpha original pero con los huecos rellenados
    # Preservamos los niveles de transparencia originales en los bordes (anti-aliasing)
    # pero forzamos el interior a 255
    new_alpha = alpha.copy()
    new_alpha[mask] = 255
    
    # 4. Crear imagen RGBA con el nuevo color y fondo NEGRO (para compatibilidad total)
    width, height = base.size
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    
    final_rgba = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Aplicar color y máscara
    mask_norm = new_alpha / 255.0
    final_rgba[..., 0] = (color_rgb[0] * mask_norm).astype(np.uint8)
    final_rgba[..., 1] = (color_rgb[1] * mask_norm).astype(np.uint8)
    final_rgba[..., 2] = (color_rgb[2] * mask_norm).astype(np.uint8)
    final_rgba[..., 3] = new_alpha
    
    result = Image.fromarray(final_rgba, mode='RGBA')
    
    # Aplicamos un SHARPEN muy ligero (el mismo que tenía el cyan_final)
    result = result.filter(ImageFilter.SHARPEN)
    
    result.save(output_path)
    return output_path

# Generar v12
# Uso la forma del Cyan para todos para garantizar paridad absoluta.
create_pure_gold_v12("#00e3fd", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v12.png")
create_pure_gold_v12("#fa02ea", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v12.png")
create_pure_gold_v12("#b0ff00", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v12.png")
