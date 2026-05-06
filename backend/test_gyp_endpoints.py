import requests
import json

BASE_URL = "http://localhost:8000"

def test_save_and_load():
    test_date = "2026-05-30"
    payload = {
        "date": test_date,
        "status": "EN PROCESO",
        "products": [
            {"qty": 2, "desc": "iPhone 17 Pro 256GB", "buyUSA": 1099.0, "sellUSD": 1400.0}
        ],
        "costs": {
            "courier": {"val": 50.0, "note": "Test courier"},
            "transfer": {"val": 10.0, "note": ""},
            "airfare": {"val": 0, "note": ""},
            "food": {"val": 0, "note": ""},
            "transport": {"val": 0, "note": ""},
            "ads": {"val": 0, "note": ""},
            "other": {"val": 5.0, "note": "Others"}
        }
    }

    print(f"Probando GUARDADO para fecha {test_date}...")
    try:
        res_save = requests.post(f"{BASE_URL}/gyp/save", json=payload)
        print(f"Respuesta Save: {res_save.status_code} - {res_save.json()}")
        
        print(f"\nProbando CARGA para fecha {test_date}...")
        res_load = requests.get(f"{BASE_URL}/gyp/load/{test_date}")
        print(f"Respuesta Load: {res_load.status_code}")
        data = res_load.json()
        if data["status"] == "success":
            print("DATOS RECUPERADOS CORRECTAMENTE:")
            print(json.dumps(data["data"], indent=2))
        else:
            print("ERROR: No se encontró el lote recién guardado.")
            
    except Exception as e:
        print(f"Error de conexión (¿Está corriendo la API?): {e}")

if __name__ == "__main__":
    test_save_and_load()
