# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import apriori, prediccion, kmeans_routes
from app.models import venta_model

app = FastAPI(
    title="API-Pan",
    description="API para análisis de ventas de panadería",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por la IP exacta si deseas restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apriori.router)
app.include_router(prediccion.router)
app.include_router(kmeans_routes.router)