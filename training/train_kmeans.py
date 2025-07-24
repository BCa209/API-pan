# training/train_kmeans.py

import json
import numpy as np
from sklearn.cluster import KMeans
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import os

# Diccionarios para codificar texto a número
hora_map = {
    "mañana": 0,
    "tarde": 1,
    "noche": 2
}

dia_map = {
    "lunes": 0,
    "martes": 1,
    "miercoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sabado": 5,
    "domingo": 6
}

# Ruta del archivo JSON
DATA_PATH = os.path.join(os.path.dirname(__file__), 'datos_fit.json')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'kmeans_model.onnx')
print(f"Buscando archivo en: {DATA_PATH}")

# Leer datos desde el JSON
with open(DATA_PATH, 'r', encoding='utf-8') as file:
    datos = json.load(file)

# Convertir datos en una lista de listas con verificación
X = []
for cliente in datos:
    try:
        compras = float(cliente["n_compras_ultimos_30_dias"])
        hora = hora_map.get(cliente["hora_preferida"].lower(), -1)
        dia = dia_map.get(cliente["dia_semana_frecuente"].lower(), -1)
        promedio = float(cliente["promedio_valor_compra"])
        recompra = float(cliente["recompra_productos"])

        if hora == -1 or dia == -1:
            raise ValueError("Valor no reconocido en hora_preferida o dia_semana_frecuente")

        X.append([compras, hora, dia, promedio, recompra])
    except Exception as e:
        print(f"[X] Error en cliente: {cliente}\n{e}")

X = np.array(X)

# Entrenar modelo KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)
""" n_clusters=3 
Cluster 0 → Clientes que compran mucho y recompran seguido.

Cluster 1 → Clientes ocasionales, compras pequeñas.

Cluster 2 → Clientes de alto valor pero baja frecuencia.
"""
# Convertir a ONNX
initial_type = [("float_input", FloatTensorType([None, 5]))]
onnx_model = convert_sklearn(kmeans, initial_types=initial_type)

# Guardar el modelo
with open(MODEL_PATH, "wb") as f:
    f.write(onnx_model.SerializeToString())

print(f"[OK] Modelo guardado en {MODEL_PATH}")
