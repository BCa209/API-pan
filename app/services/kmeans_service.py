# app/services/kmeans_service.py
import os
import json
import onnxruntime as ort
import numpy as np
from app.utils.preprocessing import transformar_dato_crudo

onnx_path = "models/kmeans_model.onnx"
# Ruta de los archivos
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'datos.json'))
# Change these lines in kmeans_service.py
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'kmeans_model.onnx')

# Diccionarios para codificación de texto a número
map_horas = {"mañana": 0, "tarde": 1, "noche": 2}
map_dias = {"lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3, "viernes": 4, "sábado": 5, "domingo": 6}

def predecir_cluster(dato: dict) -> int:
    try:
        entrada = np.array([transformar_dato_crudo(dato)], dtype=np.float32)
        session = ort.InferenceSession(MODEL_PATH)
        input_name = session.get_inputs()[0].name
        output = session.run(None, {input_name: entrada})
        return int(output[0][0])
    except Exception as e:
        raise ValueError(f"Prediction failed: {str(e)}")


def limpiar_datos(cliente):
    return [
        int(cliente.get("n_compras_ultimos_30_dias", 0)),
        map_horas.get(cliente.get("hora_preferida", "").lower(), -1),
        map_dias.get(cliente.get("dia_semana_frecuente", "").lower(), -1),
        float(cliente.get("promedio_valor_compra", 0.0)),
        int(cliente.get("recompra_productos", 0))
    ]

def predecir_desde_archivo():
    print(f"[DEBUG] Leyendo desde: {DATA_PATH}")

    # Cargar datos
    with open(DATA_PATH, "r") as f:
        datos = json.load(f)

    X = np.array([limpiar_datos(c) for c in datos], dtype=np.float32)

    # Cargar modelo ONNX
    session = ort.InferenceSession(MODEL_PATH)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    # Hacer predicciones
    resultados = session.run([output_name], {input_name: X})[0]
    return resultados.tolist()