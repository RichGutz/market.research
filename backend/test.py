import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
data = supabase.table("prices_iphone").select("*").limit(1).execute().data
if data:
    print(list(data[0].keys()))
else:
    print("No data in prices_iphone")
