import numpy as np
import onnxruntime as ort
import os
from typing import List, Dict

# Ruta al modelo ONNX de KMeans
ONNX_MODEL_PATH = os.path.join("models", "kmeans_model.onnx")

def predecir_clusters(ventas: List[Dict]) -> List[int]:
    """
    Recibe una lista de ventas, extrae características y predice los clusters usando el modelo ONNX.
    """
    if not os.path.exists(ONNX_MODEL_PATH):
        raise FileNotFoundError(f"Modelo ONNX no encontrado en: {ONNX_MODEL_PATH}")

    datos = []
    for venta in ventas:
        fila = [
            venta["hora"],
            venta["dia_semana"],
            venta["id_producto"],
            venta["cantidad"],
            venta["precio_total"]
        ]
        datos.append(fila)

    datos_np = np.array(datos, dtype=np.float32)

    # Cargar modelo ONNX
    session = ort.InferenceSession(ONNX_MODEL_PATH, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name

    # Realizar predicción
    predicciones = session.run(None, {input_name: datos_np})[0]

    return predicciones.tolist()
