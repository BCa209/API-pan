# app/models/venta_schema.py
from pydantic import BaseModel
from typing import List

class Venta(BaseModel):
    id_venta: str
    id_producto: str
    fecha_venta: str  # formato "DD-MM-YYYY"

class ListaVentas(BaseModel):
    ventas: List[Venta]
