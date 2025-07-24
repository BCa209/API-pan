# app/utils/onnx_loader.py
import onnxruntime as ort

# Cargar modelo ONNX al iniciar
session = ort.InferenceSession("models/kmeans_model.onnx", providers=["CPUExecutionProvider"])

# Obtener nombres de entrada y salida
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
