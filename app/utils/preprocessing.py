# app/utils/preprocessing.py

hora_map = {'mañana': 0, 'tarde': 1, 'noche': 2}
dia_map = {
    'lunes': 0, 'martes': 1, 'miercoles': 2,
    'jueves': 3, 'viernes': 4, 'sabado': 5, 'domingo': 6
}

# Update preprocessing.py to handle all features
def transformar_dato_crudo(dato: dict) -> list:
    return [
        int(dato.get("n_compras_ultimos_30_dias", 0)),
        hora_map.get(dato.get("hora_preferida", "").lower(), -1),
        dia_map.get(dato.get("dia_semana_frecuente", "").lower(), -1),
        float(dato.get("promedio_valor_compra", 0.0)),
        float(dato.get("recompra_productos", 0))
    ]
