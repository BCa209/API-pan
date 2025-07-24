### app/models/kmeans_model.py
from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class VentaKMeans(Base):
    __tablename__ = "ventas"

    venta_id = Column(Integer, primary_key=True, index=True)
    hora = Column(Integer)
    dia_semana = Column(Integer)
    id_producto = Column(Integer)
    cantidad = Column(Integer)
    precio_total = Column(Float)
