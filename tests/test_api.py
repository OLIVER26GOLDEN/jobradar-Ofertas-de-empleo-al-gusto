import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app.database import Base
from app.main import app, read_root
from app.deps import get_current_user
from app.routers.auth import login_user, read_me, register_user
from app.routers.alertas import create_alerta, delete_alerta, read_alertas
from app.routers.ofertas import create_oferta, read_ofertas, update_oferta_estado
from app.schemas import AlertaCreate, OfertaCreate, OfertaUpdateEstado, UserCreate, UserLogin


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
    app.dependency_overrides.clear()


def test_api_inicia_correctamente():
    assert app.title == "jobradar API"


def test_endpoint_principal_responde():
    response = read_root()

    assert response["status"] == "online"


def test_registro_login_y_usuario_autenticado(db_session):
    registered_user = register_user(
        UserCreate(
            email="USER@Example.com",
            password="supersecret",
            nombre="User Test",
        ),
        db=db_session,
    )

    assert registered_user.email == "user@example.com"
    assert registered_user.password_hash != "supersecret"

    token_payload = login_user(
        UserLogin(email="user@example.com", password="supersecret"),
        db=db_session,
    )

    assert token_payload.token_type == "bearer"
    assert token_payload.access_token

    current_user = get_current_user(
        token_payload.access_token,
        db=db_session,
    )
    me_response = read_me(current_user)

    assert me_response.email == "user@example.com"


def test_rutas_protegidas_declaran_get_current_user():
    protected_paths = {
        "/ofertas/",
        "/ofertas/{oferta_id}",
        "/ofertas/{oferta_id}/estado",
        "/alertas/",
        "/alertas/{alerta_id}",
        "/scraper/sync",
    }

    protected_routes = [
        route
        for route in app.routes
        if getattr(route, "path", None) in protected_paths
    ]

    assert protected_routes
    for route in protected_routes:
        dependencies = [dependant.call for dependant in route.dependant.dependencies]
        assert get_current_user in dependencies


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
