import base64
from PIL import Image, ImageFilter
import io
import numpy as np
from scipy import ndimage

def create_4k_vector_style(color_hex, output_path):
    # 1. Cargar la fuente 640x640
    base = Image.open("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_from_html.png").convert("RGB")
    arr = np.array(base)
    
    # 2. Extraer máscara limpia (Luminancia > 40 para evitar ruido de compresión)
    # Convertir a escala de grises para detectar forma
    gray = np.mean(arr, axis=-1)
    mask = (gray > 40).astype(bool)
    
    # 3. Rellenar huecos
    mask = ndimage.binary_fill_holes(mask)
    
    # 4. Operaciones morfológicas para suavizar bordes antes de escalar
    # Closing para unir partes sueltas, opening para limpiar
    mask = ndimage.binary_closing(mask, iterations=1)
    
    # 5. ESCALADO A 4K (2048x2048) con Lanczos
    temp_mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    hd_mask_img = temp_mask_img.resize((2048, 2048), resample=Image.LANCZOS)
    
    # 6. Binarización de la máscara HD para bordes "Vector" (Cero borrosidad)
    hd_mask_arr = np.array(hd_mask_img)
    hd_mask_final = (hd_mask_arr > 128).astype(np.uint8) * 255
    
    # 7. Opcional: Un desenfoque ultra-fino (0.5px) para evitar "jaggies" en el borde duro
    hd_mask_final_img = Image.fromarray(hd_mask_final, mode='L')
    hd_mask_final_img = hd_mask_final_img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # 8. Construir la imagen RGBA final (2048x2048)
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    
    # Imagen negra de fondo para luminancia
    width, height = (2048, 2048)
    final_rgba = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Aplicar color y alpha
    mask_hd = np.array(hd_mask_final_img)
    mask_norm = mask_hd / 255.0
    
    final_rgba[..., 0] = (color_rgb[0] * mask_norm).astype(np.uint8)
    final_rgba[..., 1] = (color_rgb[1] * mask_norm).astype(np.uint8)
    final_rgba[..., 2] = (color_rgb[2] * mask_norm).astype(np.uint8)
    final_rgba[..., 3] = mask_hd
    
    result = Image.fromarray(final_rgba, mode='RGBA')
    
    # Sharpen final para definición extrema
    result = result.filter(ImageFilter.SHARPEN)
    
    result.save(output_path)
    print(f"Generado {output_path} (Size: {os.path.getsize(output_path)} bytes)")
    return output_path

import os
# Generar v11 (4K Ultra HD)
# NOTA: Uso el Pink vibrante #fa02ea que es el que gustó, solo que ahora será nítido.
create_4k_vector_style("#00e3fd", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v11.png")
create_4k_vector_style("#fa02ea", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v11.png")
create_4k_vector_style("#b0ff00", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v11.png")
