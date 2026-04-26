import base64
import re
import os

v26_path = r'c:\Users\rguti\Tienda.APPLE.PS5\Market.Research\MASTER_INDEX_V26.html'
pure_emerald_path = r'c:\Users\rguti\Tienda.APPLE.PS5\Market.Research\logo_emerald_pure.png'

print(f"Reading V26 from: {v26_path}")
with open(v26_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract base64 from IMG_DATA[0]
match = re.search(r"const IMG_DATA = \[\s+'data:image/png;base64,(.*?)'", content, re.DOTALL)
if match:
    v26_base64 = match.group(1).replace('\n', '').replace(' ', '').replace('\r', '')
    print("Extracted base64 from V26 (length):", len(v26_base64))
else:
    print("Could not find base64 in V26")
    exit(1)

print(f"Reading pure emerald from: {pure_emerald_path}")
if os.path.exists(pure_emerald_path):
    with open(pure_emerald_path, 'rb') as f:
        pure_bytes = f.read()
    pure_base64 = base64.b64encode(pure_bytes).decode('utf-8')
    print("Pure emerald base64 (length):", len(pure_base64))
    
    if v26_base64 == pure_base64:
        print("MATCH: The silhouettes are identical.")
    else:
        print("MISMATCH: The silhouettes are different.")
        # Check if one is a substring or something (e.g. if I saved it with different compression)
        # But if physical bits are same, base64 should be same.
else:
    print("Pure emerald file not found.")
