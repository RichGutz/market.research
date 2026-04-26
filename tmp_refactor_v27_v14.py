import os
import re

html_path = "c:/Users/rguti/Tienda.APPLE.PS5/Market.Research/MASTER_INDEX_V27.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar IMG_DATA para usar archivos locales .png
# Buscamos la definición del array IMG_DATA
new_img_data = """const IMG_DATA = [
            'runner_cyan.png',
            'runner_pink.png',
            'runner_emerald.png'
        ];"""

content = re.sub(r"const IMG_DATA = \[.*?\];", new_img_data, content, flags=re.DOTALL)

# Asegurarse de que el JS use las URLs correctamente (ya lo hace si el array tiene los strings)
# Pero por si acaso, revisamos el loop o las transiciones.
# En V25, logoImg.style.maskImage = `url(${IMG_DATA[index]})`;
# Si IMG_DATA[index] es 'runner_cyan.png', el resultado es url(runner_cyan.png), lo cual es CORRECTO.

# Actualizar título de versión
content = content.replace("SYSTEM V27.6 // ULTRA-HD 4K VECTOR-SHARP", "SYSTEM V27.8 // EXTERNAL PNG ARCHITECTURE FINAL")
content = content.replace("SYSTEM V27.7 // RESTORATION-HD 640PX FINAL", "SYSTEM V27.8 // EXTERNAL PNG ARCHITECTURE FINAL")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Versión V27.8 generada en {html_path}")
