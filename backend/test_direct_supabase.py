import os
from supabase import create_client, Client
from dotenv import load_dotenv
import datetime

load_dotenv()

def test_direct_write():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)
    
    test_date = "2026-12-31"
    print(f"Insertando fila de prueba para la fecha: {test_date}")
    
    data = {
        "fecha_lote": test_date,
        "status": "EN PROCESO",
        "total_compra_usd": 100,
        "total_venta_usd": 200
    }
    
    try:
        res = supabase.table("gyp_lotes").upsert(data, on_conflict="fecha_lote").execute()
        print("Resultado de la inserción:")
        print(res.data)
        
        # Verificar lectura
        res_read = supabase.table("gyp_lotes").select("*").eq("fecha_lote", test_date).execute()
        print("\nResultado de la lectura inmediata:")
        print(res_read.data)
        
        # Limpiar
        supabase.table("gyp_lotes").delete().eq("fecha_lote", test_date).execute()
        print("\nFila de prueba eliminada.")
        
    except Exception as e:
        print(f"Error durante la prueba directa: {e}")

if __name__ == "__main__":
    test_direct_write()
