## app/services/kmeans_db.py
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from app.models.kmeans_model import Base, VentaKMeans

# 📍 Ruta de la base de datos SQLite
DB_PATH = os.path.join("data", "todos", "kmeans.sqlite")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# 🛠️ Configuración del motor SQLAlchemy
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 🧱 Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

def guardar_ventas_kmeans(data: list[dict]):
    """
    Guarda una lista de ventas en la base de datos.
    """
    session = SessionLocal()
    try:
        for venta in data:
            nueva = VentaKMeans(**venta)
            session.add(nueva)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def obtener_todas_las_ventas():
    """
    Devuelve todas las ventas almacenadas como lista de diccionarios.
    """
    if not os.path.exists(DB_PATH):
        return []

    with Session(engine) as session:
        ventas = session.scalars(select(VentaKMeans)).all()

    return [
        {
            "venta_id": v.venta_id,
            "hora": v.hora,
            "dia_semana": v.dia_semana,
            "id_producto": v.id_producto,
            "cantidad": v.cantidad,
            "precio_total": v.precio_total,
        }
        for v in ventas
    ]
