from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime

# NOTA: Este es un mock de backend preparado para ser integrado 
# en el backend principal (api_market.py) cuando haya .env disponible.

app = FastAPI(title="Mock GyP API")

class GyPProduct(BaseModel):
    cantidad: int
    descripcion: str
    precio_compra_usa: float
    precio_venta_pen: float
    prorrateo_usd: float
    ganancia_neta_usd: float

class GyPBatch(BaseModel):
    fecha: str
    tipo_cambio: float
    costos_indirectos: dict
    productos: List[GyPProduct]
    total_compra_usa: float
    total_venta_pen: float
    total_prorrateo: float
    total_ganancia_neta: float

# Diccionario en memoria simulando BD
batches_db = {}

@app.post("/batch")
def save_batch(batch: GyPBatch):
    # Simula guardar en Supabase
    batch_id = f"batch_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    batches_db[batch_id] = batch.dict()
    return {"status": "success", "batch_id": batch_id, "message": "Lote guardado en BD mockeada"}

@app.get("/batch")
def get_batches():
    # Retorna los lotes guardados en memoria
    return {"status": "success", "data": batches_db}
