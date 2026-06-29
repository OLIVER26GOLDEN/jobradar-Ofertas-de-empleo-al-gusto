from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Oferta(Base):
    __tablename__ = "ofertas"

    id            = Column(Integer, primary_key=True, index=True)
    titulo        = Column(String, nullable=False)
    empresa       = Column(String)
    ciudad        = Column(String)
    modalidad     = Column(String)           # remoto / presencial / hibrido
    salario       = Column(String)
    tecnologias   = Column(String)           # guardado como string separado por comas
    url           = Column(String, unique=True)
    estado        = Column(String, default="sin_revisar")  # sin_revisar / aplicado / guardado / descartado
    fecha_pub     = Column(String)
    creado_en     = Column(DateTime, server_default=func.now())


class Alerta(Base):
    __tablename__ = "alertas"

    id        = Column(Integer, primary_key=True, index=True)
    keyword   = Column(String, nullable=False)
    ciudad    = Column(String)
    modalidad = Column(String)
    activa    = Column(Boolean, default=True)
    creado_en = Column(DateTime, server_default=func.now())
