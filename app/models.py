import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from .database import Base


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)


class Oferta(Base):
    __tablename__ = "ofertas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    empresa = Column(String, nullable=False)
    ubicacion = Column(String, nullable=False)
    modalidad = Column(String, default="No especificado")
    salario = Column(String, default="No especificado")
    descripcion = Column(Text, nullable=True)
    enlace = Column(String, unique=True, index=True, nullable=False)
    fuente = Column(String, nullable=False)  # "InfoJobs" or "Indeed"
    estado = Column(String, default="guardado")  # "guardado", "aplicado", "descartado"
    fecha_publicacion = Column(String, nullable=True)
    creado_en = Column(DateTime, default=utc_now)

class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(Integer, primary_key=True, index=True)
    termino = Column(String, nullable=False)
    ubicacion = Column(String, default="Cualquiera")
    modalidad = Column(String, default="Cualquiera")
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=utc_now)
