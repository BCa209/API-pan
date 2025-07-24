### gen_data.py
import json
import os
import random

# Directorio y archivo destino
DATA_DIR = os.path.join(os.getcwd(), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, 'datos_fit.json')

# Opciones posibles para atributos categóricos
horas = ["mañana", "tarde", "noche"]
dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

# Generar datos simulados
datos = []
for i in range(100):
    cliente = {
        "id": f"cliente_{i:03}",
        "n_compras_ultimos_30_dias": random.randint(1, 30),
        "hora_preferida": random.choice(horas),
        "dia_semana_frecuente": random.choice(dias),
        "promedio_valor_compra": round(random.uniform(10, 200), 2),
        "recompra_productos": round(random.uniform(0, 1), 2)
    }
    datos.append(cliente)

# Guardar en archivo JSON
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)

print(f"Archivo generado en: {DATA_FILE}")
