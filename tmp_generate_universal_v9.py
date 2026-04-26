import base64
from PIL import Image, ImageFilter, ImageOps
import io
import numpy as np
from scipy import ndimage

def create_universal_mask(color_hex, output_path):
    # Usar el Cyan perfecto como plantilla
    base = Image.open("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_from_html.png").convert("RGBA")
    alpha = np.array(base.split()[3])
    
    # 1. Limpieza de máscara (Solid Core)
    mask = (alpha > 10).astype(bool)
    mask = ndimage.binary_fill_holes(mask)
    
    # Convertir de nuevo a imagen para procesar bordes
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    
    # Suavizado de bordes anti-aliasing (muy sutil)
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    # 2. Crear la imagen RGB con fondo NEGRO (para Luminancia)
    width, height = base.size
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    
    # Llenar todo de negro
    rgba_data = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Poner el color solo donde la máscara es opaca
    mask_arr = np.array(mask_img)
    mask_normalized = mask_arr / 255.0
    
    rgba_data[..., 0] = (color_rgb[0] * mask_normalized).astype(np.uint8)
    rgba_data[..., 1] = (color_rgb[1] * mask_normalized).astype(np.uint8)
    rgba_data[..., 2] = (color_rgb[2] * mask_normalized).astype(np.uint8)
    rgba_data[..., 3] = mask_arr # Canal Alpha
    
    result = Image.fromarray(rgba_data, mode='RGBA')
    
    # Sharpen para agresividad visual
    result = result.filter(ImageFilter.SHARPEN)
    
    result.save(output_path)
    return output_path

# Generar v9
create_universal_mask("#00e3fd", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v9.png")
create_universal_mask("#ed1ad9", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v9.png")
create_universal_mask("#b0ff00", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v9.png")
