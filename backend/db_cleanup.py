import os
import re
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: Credenciales de Supabase no encontradas en .env")
    exit(1)

supabase: Client = create_client(url, key)

# Configuración de limpieza (Sincronizada con scraper_peru.py)
CLEANUP_CONFIG = {
    "prices_iphone": {
        "forbidden": r'funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|organizador|sticker|decal|skin|soporte|stand|audifonos',
        "floor": 1500,
        "must_have": "iPhone"
    },
    "prices_iwatch": {
        "forbidden": r'correa|strap|funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|organizador|sticker|decal',
        "floor": 800,
        "must_have": "Watch|Series|Ultra"
    },
    "prices_ipad": {
        "forbidden": r'funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|keyboard|teclado|pencil|lapiz|soporte',
        "floor": 1200,
        "must_have": "iPad"
    },
    "prices_macbook": {
        "forbidden": r'funda|case|mica|protector|vidrio|templado|repuesto|cargador|cable|bolso|maleta|estuche|adaptador|hub|mouse',
        "floor": 2500,
        "must_have": "Macbook|Mac Book|Air|Pro"
    },
    "prices_playstation": {
        "forbidden": r'funda|case|control|mando|joystick|sticker|skin|soporte|stand|audifonos|cable|cargador',
        "floor": 1400,
        "must_have": "PlayStation|PS5"
    },
    "prices_samsung": {
        "forbidden": r'funda|case|correa|strap|mica|protector|vidrio|templado|repuesto|cargador|cable',
        "floor": 1500,
        "must_have": "Samsung|Galaxy|S26"
    }
}

def clean_database():
    print("--- Iniciando Purga de Datos Basura en Supabase ---")
    
    for table, config in CLEANUP_CONFIG.items():
        print(f"\nLimpiando tabla: {table}")
        try:
            # 1. Obtener todos los registros de la tabla
            response = supabase.table(table).select("*").execute()
            rows = response.data
            
            ids_to_delete = []
            
            for row in rows:
                title = row["scraped_title"]
                price = row["price_pen"]
                item_id = row["id"]
                
                # Check 1: Forbidden Words (Regex)
                if re.search(config["forbidden"], title, re.IGNORECASE):
                    ids_to_delete.append(item_id)
                    continue
                
                # Check 2: Price Floor
                if price < config["floor"]:
                    ids_to_delete.append(item_id)
                    continue
                
                # Check 3: Essential Keywords
                if not re.search(config["must_have"], title, re.IGNORECASE):
                    ids_to_delete.append(item_id)
                    continue
            
            if ids_to_delete:
                print(f"  -> Eliminando {len(ids_to_delete)} registros basura...")
                # Eliminar en lotes para evitar problemas de URL larga
                for i in range(0, len(ids_to_delete), 50):
                    batch = ids_to_delete[i:i+50]
                    supabase.table(table).delete().in_("id", batch).execute()
                print(f"  [OK] Tabla {table} depurada.")
            else:
                print(f"  [Info] No se encontró basura en {table}.")
                
        except Exception as e:
            print(f"  [ERROR] Al limpiar {table}: {e}")

    print("\n--- Purga Finalizada con éxito ---")

if __name__ == "__main__":
    clean_database()
