import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic import BaseModel
from typing import List, Optional
import logging
from dotenv import load_dotenv

from scraper_peru import PeruMarketScraper

# Configuración básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intentar cargar .env desde múltiples ubicaciones posibles
env_paths = [".env", "backend/.env", "../.env"]
env_loaded = False
for path in env_paths:
    if os.path.exists(path):
        load_dotenv(path)
        logger.info(f"Archivo .env cargado desde: {path}")
        env_loaded = True
        break

if not env_loaded:
    logger.warning("No se encontró ningún archivo .env. Las variables de entorno deben estar seteadas en el sistema.")

app = FastAPI(title="Tienda Apple PS5 Market API")

# Habilitar CORS para el frontend local/remoto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción a localhost y el subdominio Hostinger
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar cliente Supabase
def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Credenciales de Supabase no encontradas en .env")
    return create_client(url, key)

supabase: Client = get_supabase()

# Modelos Pydantic para la API
class CatalogItem(BaseModel):
    id: Optional[str] = None
    category: str
    model_name: str
    target_usa_price: float
    reference_url: Optional[str] = None
    specs: dict = {}

class MarginResult(BaseModel):
    catalog_id: str
    category: str
    model_name: str
    target_usa_price: float
    min_price_pen: Optional[float]
    avg_price_pen: Optional[float]
    sample_size: int
    gross_margin_pen: Optional[float] = None
    status: str = "WAITING" # WAITING, BUY, AVOID

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API de Market Research funcionando."}

@app.get("/catalog", response_model=List[CatalogItem])
def get_catalog():
    """Obtiene el catálogo base desde Supabase."""
    try:
        response = supabase.table("apple_ps5_catalog").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error obteniendo catálogo: {e}")
        raise HTTPException(status_code=500, detail="Error interconectando con Supabase")

@app.get("/margins", response_model=List[MarginResult])
def get_margins():
    """Obtiene los márgenes calculados desde la vista de Supabase."""
    try:
        response = supabase.table("vw_apple_ps5_margins").select("*").execute()
        results = []
        for row in response.data:
            margin_item = MarginResult(**row)
            
            # Lógica central del negocio (Cálculo de Ganancia Bruta)
            # Simplificado: Asume TC 1:1 si no está especificado, o requiere ajuste en Frontend/Backend.
            # Para fines del MVP pediremos el TC, o asumiremos un TC de prueba de 3.8
            TC = 3.8
            costo_usa_pen = margin_item.target_usa_price * TC
            
            if margin_item.min_price_pen:
                ganancia_bruta = margin_item.min_price_pen - costo_usa_pen
                margin_item.gross_margin_pen = round(ganancia_bruta, 2)
                
                # Semáforo simple: Si ganancia > 10% del costo, BUY
                if ganancia_bruta > (costo_usa_pen * 0.10):
                    margin_item.status = "BUY"
                elif ganancia_bruta > 0:
                    margin_item.status = "WARNING"
                else:
                    margin_item.status = "AVOID"
            
            results.append(margin_item)
            
        return results
    except Exception as e:
        logger.error(f"Error obteniendo márgenes: {e}")
        raise HTTPException(status_code=500, detail="Error leyendo vista de márgenes en Supabase")

@app.get("/market-prices")
def get_market_prices():
    """Obtiene los precios crudos scrapeados para mostrar las fuentes en el frontend."""
    try:
        response = supabase.table("vw_apple_ps5_market_prices").select("*").execute()
        return response.data
    except Exception as e:
        logger.error(f"Error obteniendo precios de mercado: {e}")
        raise HTTPException(status_code=500, detail="Error leyendo precios de Supabase")

@app.post("/scrape-all")
async def trigger_scrape_all(background_tasks: BackgroundTasks):
    """Dispara el scraper masivo asíncrono para barrer todas las categorías del mercado."""
    try:
        scraper = PeruMarketScraper()
        background_tasks.add_task(scraper.run_market_scrapers)
        return {"message": "Scraping de mercado masivo iniciado con éxito. Por favor espera unos minutos."}
    except Exception as e:
        logger.error(f"Error iniciando scraping: {e}")
        raise HTTPException(status_code=500, detail="Error al iniciar scraping")

# --- ENDPOINTS GYP ---

class GyPProductIn(BaseModel):
    qty: int
    desc: str
    buyUSA: float
    sellUSD: float

class GyPCostDetail(BaseModel):
    val: float
    note: str

class GyPCostsIn(BaseModel):
    courier: GyPCostDetail
    transfer: GyPCostDetail
    airfare: GyPCostDetail
    food: GyPCostDetail
    transport: GyPCostDetail
    ads: GyPCostDetail
    other: GyPCostDetail

class GyPBatchIn(BaseModel):
    date: str
    status: str
    products: List[GyPProductIn]
    costs: GyPCostsIn

@app.get("/gyp/load/{fecha}")
def load_gyp_batch(fecha: str):
    """Carga un lote completo de GyP desde Supabase por fecha."""
    try:
        # 1. Obtener Lote
        lote_res = supabase.table("gyp_lotes").select("*").eq("fecha_lote", fecha).execute()
        if not lote_res.data:
            return {"status": "not_found", "message": "No existe lote para esta fecha"}
        
        lote = lote_res.data[0]
        
        # 2. Obtener Productos
        prod_res = supabase.table("gyp_productos").select("*").eq("lote_fecha", fecha).execute()
        
        # 3. Obtener Costos Indirectos
        cost_res = supabase.table("gyp_costos_indirectos").select("*").eq("lote_fecha", fecha).execute()
        costs_data = cost_res.data[0] if cost_res.data else {}

        # Formatear para el frontend
        products = []
        for p in prod_res.data:
            products.append({
                "qty": p["qty"],
                "desc": p["modelo"],
                "buyUSA": float(p["compra_usd"]),
                "sellUSD": float(p["venta_usd"])
            })
        
        # Mapeo de costos (asumiendo nombres de columnas en gyp_schema.sql)
        costs = {
            "courier": {"val": float(costs_data.get("courier_usd", 0)), "note": costs_data.get("courier_nota", "")},
            "transfer": {"val": float(costs_data.get("transfer_usd", 0)), "note": costs_data.get("transfer_nota", "")},
            "airfare": {"val": float(costs_data.get("airfare_usd", 0)), "note": costs_data.get("airfare_nota", "")},
            "food": {"val": float(costs_data.get("food_usd", 0)), "note": costs_data.get("food_nota", "")},
            "transport": {"val": float(costs_data.get("transport_usd", 0)), "note": costs_data.get("transport_nota", "")},
            "ads": {"val": float(costs_data.get("ads_usd", 0)), "note": costs_data.get("ads_nota", "")},
            "other": {"val": float(costs_data.get("other_usd", 0)), "note": costs_data.get("other_nota", "")}
        }

        return {
            "status": "success",
            "data": {
                "date": fecha,
                "status": lote["status"],
                "products": products,
                "costs": costs
            }
        }
    except Exception as e:
        logger.error(f"Error cargando lote {fecha}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/gyp/save")
def save_gyp_batch(batch: GyPBatchIn):
    """Guarda o actualiza un lote completo en Supabase."""
    try:
        # 1. Upsert Lote (gyp_lotes)
        # Calculamos totales básicos para la tabla resumen
        total_compra = sum(p.qty * p.buyUSA for p in batch.products)
        total_venta = sum(p.qty * p.sellUSD for p in batch.products)
        
        lote_data = {
            "fecha_lote": batch.date,
            "status": batch.status,
            "total_compra_usd": total_compra,
            "total_venta_usd": total_venta
        }
        
        # Upsert basado en fecha_lote
        res_lote = supabase.table("gyp_lotes").upsert(lote_data, on_conflict="fecha_lote").execute()
        if hasattr(res_lote, 'error') and res_lote.error:
            raise Exception(f"Error en gyp_lotes: {res_lote.error}")

        # 2. Productos: Limpiar y Reinsertar
        res_del = supabase.table("gyp_productos").delete().eq("lote_fecha", batch.date).execute()
        if hasattr(res_del, 'error') and res_del.error:
            raise Exception(f"Error eliminando productos: {res_del.error}")
        
        if batch.products:
            new_products = []
            for p in batch.products:
                new_products.append({
                    "lote_fecha": batch.date,
                    "qty": p.qty,
                    "modelo": p.desc,
                    "compra_usd": p.buyUSA,
                    "venta_usd": p.sellUSD
                })
            res_ins = supabase.table("gyp_productos").insert(new_products).execute()
            if hasattr(res_ins, 'error') and res_ins.error:
                raise Exception(f"Error insertando productos: {res_ins.error}")

        # 3. Costos Indirectos
        c = batch.costs
        costs_data = {
            "lote_fecha": batch.date,
            "courier_usd": c.courier.val, "courier_nota": c.courier.note,
            "transfer_usd": c.transfer.val, "transfer_nota": c.transfer.note,
            "airfare_usd": c.airfare.val, "airfare_nota": c.airfare.note,
            "food_usd": c.food.val, "food_nota": c.food.note,
            "transport_usd": c.transport.val, "transport_nota": c.transport.note,
            "ads_usd": c.ads.val, "ads_nota": c.ads.note,
            "other_usd": c.other.val, "other_nota": c.other.note
        }
        res_costs = supabase.table("gyp_costos_indirectos").upsert(costs_data, on_conflict="lote_fecha").execute()
        if hasattr(res_costs, 'error') and res_costs.error:
            raise Exception(f"Error en gyp_costos: {res_costs.error}")

        return {"status": "success", "message": f"Lote {batch.date} guardado correctamente"}
    except Exception as e:
        logger.error(f"Error guardando lote {batch.date}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # NOTA: Regla global -> El usuario ejecutará uvicorn manualmente para evitar congelemientos.
    logger.info("Ejecute usando: uvicorn api_market:app --reload")
