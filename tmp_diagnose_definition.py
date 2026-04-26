from PIL import Image, ImageChops
import numpy as np

def compare_versions(perfect_path, failed_path):
    perf = Image.open(perfect_path).convert("RGBA")
    fail = Image.open(failed_path).convert("RGBA")
    
    # Extraer Alphas
    p_a = perf.split()[3]
    f_a = fail.split()[3]
    
    # Diferencia absoluta
    diff = ImageChops.difference(p_a, f_a)
    diff.save("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/debug_alpha_diff.png")
    
    # Estadísticas
    p_arr = np.array(p_a)
    f_arr = np.array(f_a)
    
    print(f"Versión Perfecta (Media Alpha): {np.mean(p_arr)}")
    print(f"Versión Fallida (Media Alpha): {np.mean(f_arr)}")
    print(f"Píxeles diferentes: {np.count_nonzero(p_arr != f_arr)}")

# Comparar el Cyan que el usuario dijo que era perfecto con mi última versión
compare_versions("c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_from_html.png", "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v6.png")
