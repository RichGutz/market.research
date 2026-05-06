import os
from supabase import create_client, Client
from dotenv import load_dotenv
import json

load_dotenv()

def list_all_batches():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)
    
    print("Listando TODOS los lotes en gyp_lotes...")
    res = supabase.table("gyp_lotes").select("*").execute()
    print(json.dumps(res.data, indent=2))

if __name__ == "__main__":
    list_all_batches()
