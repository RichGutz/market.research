import base64
import os
import re

def get_b64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

cyan_path = "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/cyan_hd_v9.png"
pink_path = "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/pink_hd_v9.png"
emerald_path = "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/emerald_hd_v9.png"

b64_cyan = get_b64(cyan_path)
b64_pink = get_b64(pink_path)
b64_emerald = get_b64(emerald_path)

html_template_path = "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V25.html"
output_path = "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V27.html"

with open(html_template_path, "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar IMG_DATA
new_img_data = f"""const IMG_DATA = [
            'data:image/png;base64,{b64_cyan}',
            'data:image/png;base64,{b64_pink}',
            'data:image/png;base64,{b64_emerald}'
        ];"""

content = re.sub(r"const IMG_DATA = \[.*?\];", new_img_data, content, flags=re.DOTALL)

# Reemplazar colores en CSS (Restaurar exactitud V25)
content = content.replace("--accent-cyan: #00e3fd;", "--accent-cyan: #00e3fd;")
content = content.replace("--accent-pink: #ff89ab;", "--accent-pink: #ed1ad9;")
content = content.replace("--accent-emerald: #b0ff00;", "--accent-emerald: #b0ff00;")

# Actualizar título de versión
content = content.replace("SYSTEM V25.3 // REVERTED TO GLOW VERSION", "SYSTEM V27.4 // UNIVERSAL-HD ALPHA-BLACK")

with open(output_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Versión V27.4 (Universal) generada en {output_path}")
