import base64
from PIL import Image, ImageFilter, ImageOps
import io
import numpy as np
from scipy import ndimage

def get_hd_silhouette(color_hex, output_path):
    # Usar el Cyan perfecto como plantilla de forma
    base = Image.open("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_from_html.png").convert("RGBA")
    
    # Extraer Alpha y limpiarlo agresivamente
    alpha = np.array(base.split()[3])
    
    # 1. Binarización para eliminar ruido grisáceo (puntos)
    mask = (alpha > 5).astype(bool)
    
    # 2. Rellenar huecos internos (los famosos "puntos")
    mask = ndimage.binary_fill_holes(mask)
    
    # 3. Restaurar suavizado en los bordes (anti-aliasing)
    # Convertir de nuevo a imagen para aplicar filtros de PIL
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    
    # Aplicar un poco de desenfoque y luego un contraste extremo para bordes nítidos pero no dentados
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=0.3))
    
    # Convertir a RGBA con el color deseado
    color_rgb = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    result = Image.new("RGBA", base.size, color_rgb + (0,))
    result.putalpha(mask_img)
    
    # Sharpen final para esa definición "Apple"
    result = result.filter(ImageFilter.SHARPEN)
    
    result.save(output_path)
    return output_path

# Colores extraídos de V25 (valores más estables)
# Cyan: #00e3fd (Validado por el usuario como perfecto)
# Pink: #ed1ad9 (De la inspección de V25)
# Emerald: #b0ff00 (Verde vibrante original)

get_hd_silhouette("#00e3fd", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v8.png")
get_hd_silhouette("#ed1ad9", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v8.png")
get_hd_silhouette("#b0ff00", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v8.png")
