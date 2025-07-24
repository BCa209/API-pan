# app/main.py
from fastapi import FastAPI
from app.routes import apriori, predict
from app.models import venta_model

app = FastAPI(
    title="API-Pan",
    description="API para análisis de ventas de panadería",
    version="1.0.0"
)

app.include_router(apriori.router)
app.include_router(predict.router)