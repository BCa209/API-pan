# app/models/input_schema.py
from pydantic import BaseModel

class ClienteInput(BaseModel):
    id: str
    n_compras_ultimos_30_dias: int
    hora_preferida: int            # Ej: 0 = mañana, 1 = tarde, 2 = noche
    dia_semana_frecuente: int      # Ej: 0 = lunes, 6 = domingo
    promedio_valor_compra: float
    recompra_productos: float      # 0.0 a 1.0

class PrediccionSalida(BaseModel):
    id: str
    cluster: int

# Update UsuarioInput to match all required features
class UsuarioInput(BaseModel):
    id: str
    n_compras_ultimos_30_dias: int
    hora_preferida: str            # "mañana", "tarde", "noche"
    dia_semana_frecuente: str      # e.g. "lunes"
    promedio_valor_compra: float
    recompra_productos: float      # 0.0 to 1.0