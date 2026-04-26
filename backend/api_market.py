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
load_dotenv()

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

if __name__ == "__main__":
    import uvicorn
    # NOTA: Regla global -> El usuario ejecutará uvicorn manualmente para evitar congelemientos.
    logger.info("Ejecute usando: uvicorn api_market:app --reload")
