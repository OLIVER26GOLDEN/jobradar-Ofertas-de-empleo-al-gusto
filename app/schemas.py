from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

# --- schemas para Ofertas ---
class OfertaBase(BaseModel):
    titulo: str
    empresa: str
    ubicacion: str
    modalidad: Optional[str] = "No especificado"
    salario: Optional[str] = "No especificado"
    descripcion: Optional[str] = None
    enlace: str
    fuente: str
    estado: Optional[str] = "guardado"
    fecha_publicacion: Optional[str] = None

class OfertaCreate(OfertaBase):
    pass

class OfertaUpdateEstado(BaseModel):
    estado: str  # "guardado", "aplicado", "descartado"

class Oferta(OfertaBase):
    id: int
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)


# --- schemas para Alertas ---
class AlertaBase(BaseModel):
    termino: str
    ubicacion: Optional[str] = "Cualquiera"
    modalidad: Optional[str] = "Cualquiera"
    activo: Optional[bool] = True

class AlertaCreate(AlertaBase):
    pass

class Alerta(AlertaBase):
    id: int
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)
