# app/services/apriori_service.py
import json
import os
from collections import defaultdict
from typing import List, Dict, Any
import pandas as pd
from app.models.database import get_session_for_date

from mlxtend.frequent_patterns import apriori, association_rules
from sqlalchemy.orm import Session
from app.models.venta_model import VentaORM

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data')


def ejecutar_apriori_sqlite(fecha: str, min_support=0.1, min_confidence=0.5):
    db: Session = get_session_for_date(fecha)
    registros = db.query(VentaORM).filter(VentaORM.fecha_venta == fecha).all()

    transacciones = defaultdict(set)
    for r in registros:
        transacciones[r.id_venta].add(r.id_producto)

    lista_transacciones = list(transacciones.values())
    if not lista_transacciones:
        return {"mensaje": f"No hay datos para la fecha {fecha}"}

    all_items = sorted({item for t in lista_transacciones for item in t})
    df = pd.DataFrame([{item: item in t for item in all_items} for t in lista_transacciones])

    frecuentes = apriori(df, min_support=min_support, use_colnames=True)
    reglas = association_rules(frecuentes, metric="confidence", min_threshold=min_confidence)

    resultados = []
    for _, row in reglas.iterrows():
        resultados.append({
            "antecedente": list(row["antecedents"]),
            "consecuente": list(row["consequents"]),
            "soporte": round(row["support"], 4),
            "confianza": round(row["confidence"], 4),
            "lift": round(row["lift"], 4)
        })

    carpeta = os.path.join(DATA_PATH, fecha)
    os.makedirs(carpeta, exist_ok=True)
    path_resultado = os.path.join(carpeta, "resultados_apriori.json")
    with open(path_resultado, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    return {
        "mensaje": f"{len(resultados)} reglas generadas y guardadas en {path_resultado}",
        "reglas": resultados
    }


def aplicar_apriori(fecha: str, min_support=0.1, min_confidence=0.5):
    return ejecutar_apriori_sqlite(fecha, min_support, min_confidence)


def aplicar_apriori_todos():
    db: Session = get_session_for_date(fecha)
    fechas = db.query(VentaORM.fecha_venta).distinct().all()
    fechas_unicas = sorted(set(f[0] for f in fechas))

    resultados_totales = {}
    for fecha in fechas_unicas:
        resultado = ejecutar_apriori_sqlite(fecha)
        resultados_totales[fecha] = resultado.get("reglas", [])

    path_global = os.path.join(DATA_PATH, "resultados_apriori_todos.json")
    with open(path_global, 'w', encoding='utf-8') as f:
        json.dump(resultados_totales, f, indent=4, ensure_ascii=False)

    return {
        "mensaje": f"Apriori aplicado a {len(fechas_unicas)} fechas",
        "resultados": resultados_totales
    }


def guardar_ventas_y_aplicar_apriori(fecha: str, ventas: List[Dict[str, Any]]):
    db: Session = get_session_for_date(fecha)
    try:
        for v in ventas:
            nueva = VentaORM(
                id_venta=int(v["id_venta"]),
                id_producto=int(v["id_producto"]),
                fecha_venta=fecha
            )
            db.add(nueva)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return ejecutar_apriori_sqlite(fecha)
