from fastapi import APIRouter, Query, HTTPException
from app.services.apriori_service import aplicar_apriori, aplicar_apriori_todos, guardar_ventas_y_aplicar_apriori
from typing import List, Dict, Any

router = APIRouter()

@router.get("/apriori/{fecha}")
def ejecutar_apriori_por_fecha(
    fecha: str,
    min_support: float = Query(0.1, ge=0.01, le=1.0, description="Soporte mínimo entre 0.01 y 1.0"),
    min_confidence: float = Query(0.5, ge=0.0, le=1.0, description="Confianza mínima entre 0.0 y 1.0")
):
    try:
        resultado = aplicar_apriori(fecha)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/apriori/todos")
def ejecutar_apriori_para_todos():
    try:
        resultado = aplicar_apriori_todos()
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/venta/{fecha}")
def registrar_ventas_y_aplicar_apriori(
    fecha: str,
    ventas: List[Dict[str, Any]]
):
    """
    Ejemplo del body JSON esperado:
    [
        { "id_venta": 1, "producto": { "id_producto": 1 } },
        { "id_venta": 1, "producto": { "id_producto": 2 } },
        { "id_venta": 2, "producto": { "id_producto": 1 } }
    ]
    """
    try:
        return guardar_ventas_y_aplicar_apriori(fecha, ventas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))