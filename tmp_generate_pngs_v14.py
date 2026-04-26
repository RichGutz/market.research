import base64
from PIL import Image, ImageFilter
import io
import numpy as np
from scipy import ndimage

def create_external_png_v14(color_hex, output_path):
    # 1. Cargar el Cyan de referencia (640x640)
    # Asumo que este es el que tiene la definición que al usuario le gusta.
    base = Image.open("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_from_html.png").convert("RGB")
    arr = np.array(base)
    
    # 2. Extraer máscara de luminancia (sin tocar los bordes)
    gray = np.mean(arr, axis=-1)
    mask = (gray > 10).astype(bool)
    
    # 3. Rellenado morfológico quirúrgico de puntos internos
    mask = ndimage.binary_fill_holes(mask)
    
    # 4. Crear el canal Alpha basado en la máscara limpia
    # Usamos la máscara como alpha directo para preservar la definición de la forma
    mask_img = (mask * 255).astype(np.uint8)
    
    # 5. Construir la imagen con el color exacto y fondo negro
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    width, height = base.size
    
    final_rgba = np.zeros((height, width, 4), dtype=np.uint8)
    
    # Llenamos con el color pero solo donde dice la máscara
    final_rgba[mask, 0] = color_rgb[0]
    final_rgba[mask, 1] = color_rgb[1]
    final_rgba[mask, 2] = color_rgb[2]
    final_rgba[..., 3] = mask_img # Canal Alpha
    
    result = Image.fromarray(final_rgba, mode='RGBA')
    
    # NO APLICAMOS NINGUN FILTRO ADICIONAL (Ni sharpen, ni blur) para no perder definición
    result.save(output_path)
    print(f"Creado {output_path}")

# Generar archivos externos
# NOTA: Uso los colores de la V25 equilibrada para el Pink
create_external_png_v14("#00e3fd", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_cyan.png")
create_external_png_v14("#ed1ad9", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_pink.png")
create_external_png_v14("#b0ff00", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/runner_emerald.png")
