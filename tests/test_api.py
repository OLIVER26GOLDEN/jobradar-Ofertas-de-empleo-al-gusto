import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import Base
from app.main import app, read_root
from app.routers.alertas import create_alerta, delete_alerta, read_alertas
from app.routers.ofertas import create_oferta, read_ofertas, update_oferta_estado
from app.schemas import AlertaCreate, OfertaCreate, OfertaUpdateEstado


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


def test_api_inicia_correctamente():
    assert app.title == "jobradar API"


def test_endpoint_principal_responde():
    response = read_root()

    assert response["status"] == "online"


def test_endpoint_ofertas_responde_y_lista_ofertas(db_session):
    response = read_ofertas(db=db_session)

    assert isinstance(response, list)


def test_crear_y_listar_oferta(db_session):
    payload = OfertaCreate(**{
        "titulo": "Backend Python Developer",
        "empresa": "JobRadar Labs",
        "ubicacion": "Madrid",
        "modalidad": "Remoto",
        "salario": "No especificado",
        "descripcion": "Desarrollo de APIs con FastAPI.",
        "enlace": "https://example.com/ofertas/backend-python-developer",
        "fuente": "Test",
        "estado": "guardado",
        "fecha_publicacion": "2026-06-28",
    })

    created_offer = create_oferta(payload, db=db_session)

    assert created_offer.titulo == payload.titulo
    assert created_offer.empresa == payload.empresa
    assert created_offer.id is not None

    list_response = read_ofertas(db=db_session)
    assert any(offer.enlace == payload.enlace for offer in list_response)


def test_actualizar_estado_oferta(db_session):
    payload = OfertaCreate(**{
        "titulo": "Backend Python Developer",
        "empresa": "JobRadar Labs",
        "ubicacion": "Madrid",
        "modalidad": "Remoto",
        "salario": "No especificado",
        "descripcion": "Desarrollo de APIs con FastAPI.",
        "enlace": "https://example.com/ofertas/backend-python-state",
        "fuente": "Test",
        "estado": "guardado",
        "fecha_publicacion": "2026-06-28",
    })
    created = create_oferta(payload, db=db_session)

    response = update_oferta_estado(
        created.id,
        OfertaUpdateEstado(estado="aplicado"),
        db=db_session,
    )

    assert response.estado == "aplicado"


def test_crear_y_borrar_alerta(db_session):
    payload = AlertaCreate(**{
        "termino": "python",
        "ubicacion": "Madrid",
        "modalidad": "Remoto",
        "activo": True,
    })

    created_alert = create_alerta(payload, db=db_session)
    assert created_alert.id is not None

    list_response = read_alertas(db=db_session)
    assert any(alert.id == created_alert.id for alert in list_response)

    delete_response = delete_alerta(created_alert.id, db=db_session)
    assert delete_response is None
