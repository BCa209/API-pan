# app/models/venta_model.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class VentaORM(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_venta = Column(Integer)
    id_producto = Column(Integer)
    fecha_venta = Column(String)
