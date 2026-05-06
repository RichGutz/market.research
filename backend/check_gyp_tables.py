import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def check_gyp_tables():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("Error: No se encontraron credenciales en .env")
        return

    supabase = create_client(url, key)
    
    tables = ["gyp_lotes", "gyp_productos", "gyp_costos_indirectos"]
    for table in tables:
        try:
            # Intento de select simple de 1 fila
            response = supabase.table(table).select("*").limit(1).execute()
            print(f"Tabla '{table}': OK (Existe)")
        except Exception as e:
            print(f"Tabla '{table}': ERROR - {e}")

if __name__ == "__main__":
    check_gyp_tables()
