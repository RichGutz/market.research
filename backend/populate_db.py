import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("Error: Credenciales de Supabase no encontradas en .env")
    exit(1)

supabase: Client = create_client(url, key)

def populate():
    print("Conectando a Supabase...")
    
    # Datos de prueba para el catálogo
    catalog_items = [
        # --- iPHONE ---
        {"category": "iPhone", "model_name": "iPhone 17 128GB", "target_usa_price": 799.00, "specs": {"memoria": "128GB", "chip": "A19", "pantalla": "6.1 Super Retina XDR"}},
        {"category": "iPhone", "model_name": "iPhone 17 Pro 256GB", "target_usa_price": 1099.00, "specs": {"memoria": "256GB", "chip": "A19 Pro", "pantalla": "6.3 ProMotion"}},
        {"category": "iPhone", "model_name": "iPhone 17 Pro Max 256GB", "target_usa_price": 1199.00, "specs": {"memoria": "256GB", "chip": "A19 Pro", "pantalla": "6.9 ProMotion"}},
        {"category": "iPhone", "model_name": "iPhone 16 128GB", "target_usa_price": 799.00, "specs": {"memoria": "128GB", "chip": "A18", "pantalla": "6.1 Super Retina XDR"}},
        {"category": "iPhone", "model_name": "iPhone 16 Pro 256GB", "target_usa_price": 1099.00, "specs": {"memoria": "256GB", "chip": "A18 Pro", "pantalla": "6.3 ProMotion"}},
        {"category": "iPhone", "model_name": "iPhone 16 Pro Max 256GB", "target_usa_price": 1199.00, "specs": {"memoria": "256GB", "chip": "A18 Pro", "pantalla": "6.9 ProMotion"}},
        
        # --- MACBOOK ---
        {"category": "Macbook", "model_name": "MacBook Air M5 13-inch 8GB 256GB", "target_usa_price": 1099.00, "specs": {"procesador": "M5", "ram": "8GB", "memoria": "256GB"}},
        {"category": "Macbook", "model_name": "MacBook Air M5 15-inch 16GB 512GB", "target_usa_price": 1499.00, "specs": {"procesador": "M5", "ram": "16GB", "memoria": "512GB"}},
        {"category": "Macbook", "model_name": "MacBook Pro 14-inch M5 Pro 18GB 512GB", "target_usa_price": 1999.00, "specs": {"procesador": "M5 Pro", "ram": "18GB", "memoria": "512GB"}},
        {"category": "Macbook", "model_name": "MacBook Air M3 13-inch 8GB 256GB", "target_usa_price": 1099.00, "specs": {"procesador": "M3", "ram": "8GB", "memoria": "256GB"}},
        {"category": "Macbook", "model_name": "MacBook Air M3 15-inch 16GB 512GB", "target_usa_price": 1499.00, "specs": {"procesador": "M3", "ram": "16GB", "memoria": "512GB"}},
        {"category": "Macbook", "model_name": "MacBook Pro 14-inch M3 Pro 18GB 512GB", "target_usa_price": 1999.00, "specs": {"procesador": "M3 Pro", "ram": "18GB", "memoria": "512GB"}},
        {"category": "Macbook", "model_name": "MacBook Pro 16-inch M3 Max 36GB 1TB", "target_usa_price": 3499.00, "specs": {"procesador": "M3 Max", "ram": "36GB", "memoria": "1TB"}},
        
        # --- iWATCH (Filtro Crítico) ---
        {"category": "iWatch", "model_name": "Apple Watch Series 11 42mm GPS", "target_usa_price": 399.00, "specs": {"chip": "S11", "pantalla": "OLED Wide-angle"}},
        {"category": "iWatch", "model_name": "Apple Watch Series 10 46mm GPS", "target_usa_price": 429.00, "specs": {"chip": "S10", "pantalla": "OLED Wide-angle"}},
        {"category": "iWatch", "model_name": "Apple Watch Series 9 45mm GPS", "target_usa_price": 329.00, "specs": {"chip": "S9", "pantalla": "Retina Always-on"}},
        {"category": "iWatch", "model_name": "Apple Watch Ultra 2", "target_usa_price": 799.00, "specs": {"batería": "36-72 hrs", "brillo": "3000 nits"}},
        
        # --- iPAD ---
        {"category": "iPad", "model_name": "iPad Pro 13-inch M5 256GB", "target_usa_price": 1299.00, "specs": {"procesador": "M5", "pantalla": "OLED Tandem"}},
        {"category": "iPad", "model_name": "iPad Pro 11-inch M4 256GB", "target_usa_price": 999.00, "specs": {"procesador": "M4", "pantalla": "OLED Tandem"}},
        {"category": "iPad", "model_name": "iPad Pro 13-inch M4 256GB", "target_usa_price": 1299.00, "specs": {"procesador": "M4", "pantalla": "OLED Tandem"}},
        {"category": "iPad", "model_name": "iPad Air 11-inch M2 128GB", "target_usa_price": 599.00, "specs": {"procesador": "M2", "pantalla": "Liquid Retina"}},

        # --- PLAYSTATION ---
        {"category": "PlayStation", "model_name": "PlayStation 5 Disc Edition", "target_usa_price": 499.00, "specs": {"tipo": "Disco", "memoria": "825GB"}},
        {"category": "PlayStation", "model_name": "PlayStation 5 Slim Digital", "target_usa_price": 399.00, "specs": {"tipo": "Digital", "memoria": "1TB"}},
        {"category": "PlayStation", "model_name": "PlayStation 5 Slim Standard", "target_usa_price": 499.00, "specs": {"tipo": "Disco", "memoria": "1TB"}},
        {"category": "PlayStation", "model_name": "PlayStation 5 Pro", "target_usa_price": 699.00, "specs": {"tipo": "Pro", "memoria": "2TB", "GPU": "Aumentada"}},

        # --- SAMSUNG ---
        {"category": "Samsung", "model_name": "Samsung Galaxy S26 Ultra 256GB", "target_usa_price": 1199.00, "specs": {"procesador": "SD 8 Gen 5", "pantalla": "6.8 2X"}},
        {"category": "Samsung", "model_name": "Samsung Galaxy S26 Ultra 512GB", "target_usa_price": 1299.00, "specs": {"procesador": "SD 8 Gen 5", "pantalla": "6.8 2X"}},

        # --- AIRPODS ---
        {"category": "AirPods", "model_name": "Apple AirPods (2nd Gen)", "target_usa_price": 129.00, "specs": {"chip": "H1", "bateria": "24 hrs"}},
        {"category": "AirPods", "model_name": "Apple AirPods (3rd Gen)", "target_usa_price": 169.00, "specs": {"chip": "H1", "audio": "Espacial"}},
        {"category": "AirPods", "model_name": "Apple AirPods 4", "target_usa_price": 129.00, "specs": {"chip": "H2", "tipo": "Standard"}},
        {"category": "AirPods", "model_name": "Apple AirPods 4 con ANC", "target_usa_price": 179.00, "specs": {"chip": "H2", "tipo": "ANC"}},
        {"category": "AirPods", "model_name": "Apple AirPods Pro 2", "target_usa_price": 249.00, "specs": {"chip": "H2", "tipo": "Pro"}},
        {"category": "AirPods", "model_name": "Apple AirPods Max", "target_usa_price": 549.00, "specs": {"chip": "H1", "tipo": "Over-Ear"}}
    ]
    
    for item in catalog_items:
        try:
            # Upsert para no fallar si ya existen
            res = supabase.table("apple_ps5_catalog").upsert(
                item, 
                on_conflict="model_name"
            ).execute()
            print(f"Éxito procesando: {item['model_name']} -> {res.data}")
        except Exception as e:
            print(f"Error procesando {item['model_name']}: {e}")

    print("\nVerificando tabla apple_ps5_catalog:")
    try:
        res = supabase.table("apple_ps5_catalog").select("*").execute()
        for row in res.data:
            print(f"- {row['category']}: {row['model_name']} ($ {row['target_usa_price']})")
    except Exception as e:
        print(f"Error consultando catálogo: {e}")

if __name__ == "__main__":
    populate()
