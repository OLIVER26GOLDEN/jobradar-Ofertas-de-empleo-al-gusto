from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import ofertas, alertas
from app.services.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al arrancar
    Base.metadata.create_all(bind=engine)
    start_scheduler()
    yield
    # Al cerrar
    stop_scheduler()


app = FastAPI(
    title="jobradar 🎯",
    description="Radar de ofertas de empleo — Infojobs API + alertas por Telegram",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(ofertas.router)
app.include_router(alertas.router)


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "jobradar activo 🎯 — visita /docs para la documentación"}
