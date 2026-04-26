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

TABLES = [
    "prices_iphone", "prices_iwatch", "prices_ipad", 
    "prices_macbook", "prices_playstation", "prices_samsung"
]

def audit_ishop_results():
    print("--- Auditoría de Resultados iShop en Supabase ---")
    total_ishop = 0
    
    for table in TABLES:
        try:
            # Contar resultados de iShop
            response = supabase.table(table).select("scraped_title, store, price_pen").eq("store", "iShop").execute()
            results = response.data
            count = len(results)
            total_ishop += count
            
            print(f"\nTabla: {table}")
            print(f"  Resultados iShop encontrados: {count}")
            for res in results:
                print(f"    - {res['scraped_title']} (S/ {res['price_pen']})")
                
        except Exception as e:
            print(f"  [ERROR] Consultando {table}: {e}")

    print(f"\nTotal Global iShop: {total_ishop}")
    print("-------------------------------------------------")

if __name__ == "__main__":
    audit_ishop_results()
