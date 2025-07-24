# app/routes/predict.py
from fastapi import APIRouter
from app.services.kmeans_service import predecir_cluster, predecir_desde_archivo
from app.models.input_schema import UsuarioInput

router = APIRouter()

@router.post("/predict")
def hacer_prediccion(usuario: UsuarioInput):
    cluster = predecir_cluster(usuario.dict())
    return {"cluster": cluster}

@router.get("/predecir-todos", tags=["Predicción"])
def predecir_todos():
    resultados = predecir_desde_archivo()
    return {"predicciones": resultados}