from pydantic import BaseModel
from typing import Optional


# ── Ofertas ──────────────────────────────────────────────

class OfertaOut(BaseModel):
    id:          int
    titulo:      str
    empresa:     Optional[str]
    ciudad:      Optional[str]
    modalidad:   Optional[str]
    salario:     Optional[str]
    tecnologias: Optional[str]
    url:         Optional[str]
    estado:      str
    fecha_pub:   Optional[str]

    model_config = {"from_attributes": True}


class OfertaEstado(BaseModel):
    estado: str  # sin_revisar / aplicado / guardado / descartado


# ── Alertas ──────────────────────────────────────────────

class AlertaCreate(BaseModel):
    keyword:   str
    ciudad:    Optional[str] = None
    modalidad: Optional[str] = None


class AlertaOut(BaseModel):
    id:        int
    keyword:   str
    ciudad:    Optional[str]
    modalidad: Optional[str]
    activa:    bool

    model_config = {"from_attributes": True}
