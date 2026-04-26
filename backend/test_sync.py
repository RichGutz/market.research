import os
import requests
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
headers = {"apikey": key, "Authorization": f"Bearer {key}"}

print("Consultando vw_apple_ps5_market_prices...")
res = requests.get(f"{url}/rest/v1/vw_apple_ps5_market_prices?limit=1", headers=headers)
if res.ok and res.json():
    print(res.json()[0])
else:
    print("Error vw_apple_ps5_market_prices:", res.text)
