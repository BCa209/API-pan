# app/services/kmeans_service.py
from app.utils.onnx_loader import predecir_cluster

def generar_vector_venta(venta: dict) -> list[float]:
    """
    Transforma los datos de una venta en el vector esperado por el modelo KMeans.
    Se espera que el diccionario contenga: cantidad_total, monto_total, hora, es_finde
    """
    try:
        return [
            float(venta["cantidad_total"]),
            float(venta["monto_total"]),
            float(venta["hora"]),
            float(venta["es_finde"]),
        ]
    except KeyError as e:
        raise ValueError(f"Falta el campo requerido: {e}")
    except Exception as e:
        raise ValueError(f"Error al generar vector: {e}")

def predecir_segmento(venta: dict) -> dict:
    """
    Predice el segmento de cliente (cluster) según los datos de la venta.
    """
    vector = generar_vector_venta(venta)
    cluster = predecir_cluster(vector)

    etiquetas = {
        0: "Compras pequeñas matutinas",
        1: "Compras familiares de fin de semana",
        2: "Snacks de tarde"
    }

    return {
        "cluster": int(cluster),
        "segmento": etiquetas.get(int(cluster), "Desconocido")
    }
