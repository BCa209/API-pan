import os
import onnxruntime as ort
import numpy as np
from typing import List

# Ruta segura al modelo ONNX
ONNX_MODEL_PATH = os.path.join("models", "kmeans_model.onnx")

# Inicializa la sesión ONNX al cargar el módulo
if not os.path.exists(ONNX_MODEL_PATH):
    raise FileNotFoundError(f"Modelo ONNX no encontrado en: {ONNX_MODEL_PATH}")

session = ort.InferenceSession(ONNX_MODEL_PATH, providers=["CPUExecutionProvider"])

def predecir_cluster(vector: List[float]) -> int:
    """
    Predice el clúster de un solo vector usando el modelo KMeans ONNX.
    """
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    input_data = np.array([vector], dtype=np.float32)

    pred = session.run([output_name], {input_name: input_data})[0]
    return int(pred[0])
