import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.venta_model import Base

def get_engine_for_date(fecha: str):
    folder = os.path.join(os.path.dirname(__file__), '..', '..', 'data', fecha)
    os.makedirs(folder, exist_ok=True)
    db_path = os.path.join(folder, 'ventas.sqlite')
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    return engine

def get_session_for_date(fecha: str):
    engine = get_engine_for_date(fecha)
    Base.metadata.create_all(engine)  # 👈 Crea la tabla si no existe
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
