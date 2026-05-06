import os
from supabase import create_client, Client
from dotenv import load_dotenv
import json

load_dotenv()

def check_date_data(date_str):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)
    
    print(f"Buscando datos para la fecha: {date_str}")
    
    # 1. Lotes
    res_lote = supabase.table("gyp_lotes").select("*").eq("fecha_lote", date_str).execute()
    print(f"\n--- gyp_lotes ---")
    print(json.dumps(res_lote.data, indent=2))
    
    # 2. Productos
    res_prod = supabase.table("gyp_productos").select("*").eq("lote_fecha", date_str).execute()
    print(f"\n--- gyp_productos ---")
    print(json.dumps(res_prod.data, indent=2))
    
    # 3. Costos
    res_cost = supabase.table("gyp_costos_indirectos").select("*").eq("lote_fecha", date_str).execute()
    print(f"\n--- gyp_costos_indirectos ---")
    print(json.dumps(res_cost.data, indent=2))

if __name__ == "__main__":
    check_date_data("2026-04-30")
