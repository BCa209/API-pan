### app/routes/kmeans_routes.py
from fastapi import APIRouter, HTTPException
from app.services.kmeans_db import guardar_ventas_kmeans, obtener_todas_las_ventas
from app.utils.kmeans_predictor import predecir_clusters
from app.utils.cluster_labels import get_cluster_label

router = APIRouter()


@router.post("/kmeans/guardar", tags=["KMeans"])
def guardar_datos_kmeans(ventas: list[dict]):
    """
    Guarda una lista de ventas en la base de datos kmeans.sqlite.
    """
    try:
        guardar_ventas_kmeans(ventas)
        return {"mensaje": "Ventas guardadas correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar ventas: {str(e)}")


@router.get("/kmeans/clusterizados", tags=["KMeans"])
def obtener_clusterizaciones():
    """
    Retorna las ventas con su predicción de cluster y descripción,
    y guarda los resultados en un archivo JSON junto a la base de datos.
    """
    ventas = obtener_todas_las_ventas()

    if not ventas:
        return {"mensaje": "No hay ventas registradas."}

    try:
        predicciones = predecir_clusters(ventas)

        resultado = []
        for venta, cluster_id in zip(ventas, predicciones):
            resultado.append({
                "venta_id": venta["venta_id"],
                "hora": venta["hora"],
                "dia_semana": venta["dia_semana"],
                "id_producto": venta["id_producto"],
                "cantidad": venta["cantidad"],
                "precio_total": venta["precio_total"],
                "cluster": int(cluster_id),
                "descripcion": get_cluster_label(cluster_id)
            })

        # ⬇ Guardar resultado como JSON
        import os, json
        ruta_json = os.path.join("data", "todos", "kmeans_result.json")
        os.makedirs(os.path.dirname(ruta_json), exist_ok=True)
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump({"resultados": resultado}, f, indent=2, ensure_ascii=False)

        return {"resultados": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al predecir clusters: {str(e)}")
