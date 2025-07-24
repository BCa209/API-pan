# app/routes/prediccion.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.kmeans_service import predecir_segmento

router = APIRouter()

class VentaInput(BaseModel):
    venta_id: int
    hora: int
    dia_semana: int
    id_producto: int
    cantidad: int
    precio_total: float

@router.post("/predecir-cluster", tags=["KMeans"])
def predecir_cluster(venta: VentaInput):
    """
    Retorna la predicción del cluster para una venta específica.
    """
    try:
        return predecir_segmento(venta.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir cluster: {str(e)}")
