# JobRadar

JobRadar es una aplicacion SaaS multiusuario para crear alertas de empleo, gestionar busquedas y preparar integraciones futuras con fuentes externas como InfoJobs. El proyecto combina una API REST con FastAPI, una base de datos PostgreSQL y un dashboard autenticado en Streamlit.

El estado actual del proyecto se centra en la base SaaS: autenticacion JWT, usuarios, alertas por usuario, dashboard autenticado y preparacion de scrapers con datos mock cuando no existen credenciales reales.

## Objetivo

El objetivo de JobRadar es centralizar alertas de empleo personalizadas por usuario y, progresivamente, automatizar la deteccion de ofertas relevantes desde fuentes externas, con notificaciones futuras por Telegram o email.

En esta fase, el foco es tener una base estable:

- API protegida con JWT.
- Base de datos preparada para multiples usuarios.
- CRUD completo de alertas.
- Dashboard que consume la API por HTTP.
- Preparacion para conectar InfoJobs mas adelante sin hardcodear credenciales.

## Caracteristicas Implementadas

- Backend con FastAPI.
- Autenticacion JWT:
  - Registro de usuario.
  - Login.
  - Endpoint `/auth/me`.
- Base de datos con SQLAlchemy.
- PostgreSQL con Docker Compose.
- Modelo `User` existente y funcional.
- Modelo `Alert` asociado a usuario.
- Modelos base preparados:
  - `User`
  - `Alert`
  - `JobOffer`
  - `NotificationLog`
  - `ScraperRun`
- CRUD completo de alertas:
  - Crear.
  - Listar.
  - Ver detalle.
  - Editar.
  - Activar.
  - Desactivar.
  - Eliminar.
- Aislamiento multiusuario: cada usuario solo ve y modifica sus propias alertas.
- Dashboard autenticado en Streamlit.
- Dashboard comunicado unicamente con FastAPI mediante `requests`.
- Preparacion de InfoJobs:
  - Variables de entorno documentadas.
  - Funcion de busqueda preparada.
  - Fallback a datos mock si no hay credenciales.
- Tests basicos para API, auth, alertas y scrapers.
- Docker Compose para API, dashboard y PostgreSQL.

## Arquitectura

```text
Usuario
  |
  v
Dashboard Streamlit
  |
  | HTTP + JWT
  v
FastAPI
  |
  | SQLAlchemy
  v
PostgreSQL
```

Componentes principales:

- `dashboard/app.py`: interfaz web autenticada.
- `app/main.py`: entrada principal de FastAPI.
- `app/routers/`: endpoints REST.
- `app/models.py`: modelos SQLAlchemy.
- `app/schemas.py`: schemas Pydantic.
- `app/scraper/infojobs.py`: preparacion para la API de InfoJobs.
- `migrations/`: migraciones Alembic.
- `tests/`: pruebas automatizadas.

## Tecnologias Utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic
- Streamlit
- Requests
- Pytest
- Docker
- Docker Compose

## Estructura de Carpetas

```text
jobradar/
├── app/
│   ├── core/
│   │   └── security.py
│   ├── routers/
│   │   ├── alertas.py
│   │   ├── auth.py
│   │   ├── notificaciones.py
│   │   └── ofertas.py
│   ├── scraper/
│   │   ├── indeed.py
│   │   └── infojobs.py
│   ├── services/
│   │   ├── email.py
│   │   ├── notifications.py
│   │   ├── scheduler.py
│   │   └── telegram.py
│   ├── database.py
│   ├── deps.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── dashboard/
│   ├── components/
│   ├── app.py
│   └── main.py
├── migrations/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── test_api.py
│   ├── test_scraper.py
│   └── test_sync.py
├── .env.example
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements-api.txt
├── requirements-dashboard.txt
├── requirements.txt
└── README.md
```

## Instalacion

### 1. Clonar el repositorio

```bash
git clone https://github.com/Ciscojes/jobradar.git
cd jobradar
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Para instalaciones separadas:

```bash
pip install -r requirements-api.txt
pip install -r requirements-dashboard.txt
```

### 4. Crear archivo de entorno

```bash
cp .env.example .env
```

## Variables de Entorno

Ejemplo basado en `.env.example`:

```env
# Opcion rapida para desarrollo:
DATABASE_URL=sqlite:///./jobradar.db

# Opcion SaaS local con Docker Compose:
# DATABASE_URL=postgresql://jobradar:jobradar@localhost:5432/jobradar

SECRET_KEY=cambia-este-valor-en-produccion
ACCESS_TOKEN_EXPIRE_MINUTES=60

# InfoJobs: opcional. Si faltan, se usan datos de prueba.
INFOJOBS_CLIENT_ID=
INFOJOBS_CLIENT_SECRET=
INFOJOBS_REDIRECT_URI=http://localhost:8000/auth/infojobs/callback

# Telegram: pendiente. Cada usuario podra configurar su canal.
TELEGRAM_BOT_TOKEN=

# Email SMTP: pendiente. Si faltan, el envio se simulara.
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
EMAIL_FROM=

# Scheduler: pendiente/desactivado por defecto.
SCRAPER_SCHEDULER_ENABLED=false
SCRAPER_INTERVAL_MINUTES=360
SCRAPER_DEFAULT_QUERY=python

# Dashboard
API_URL=http://localhost:8000
```

Notas:

- En Docker Compose, el dashboard debe usar `API_URL=http://api:8000`.
- Si `INFOJOBS_CLIENT_ID` o `INFOJOBS_CLIENT_SECRET` estan vacios, JobRadar usa datos mock.
- No se deben hardcodear credenciales reales en el repositorio.

## Uso con Docker Compose

Levantar todos los servicios:

```bash
docker compose up -d
```

Servicios disponibles:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Dashboard: `http://localhost:8501`
- PostgreSQL: `localhost:5432`

Ver estado:

```bash
docker compose ps
```

Ver logs:

```bash
docker compose logs -f api
docker compose logs -f dashboard
docker compose logs -f postgres
```

Detener servicios:

```bash
docker compose down
```

## Ejecutar la API

Sin Docker:

```bash
uvicorn app.main:app --reload
```

La API queda disponible en:

- `http://localhost:8000`
- `http://localhost:8000/docs`

## Ejecutar el Dashboard

Sin Docker:

```bash
API_URL=http://localhost:8000 streamlit run dashboard/app.py
```

El dashboard queda disponible en:

```text
http://localhost:8501
```

El dashboard no se conecta directamente a la base de datos. Todas las operaciones pasan por FastAPI usando HTTP y JWT.

## Capturas

Marcadores para futuras imagenes:

### Login

```text
docs/images/dashboard-login.png
```

### Registro

```text
docs/images/dashboard-register.png
```

### Dashboard Autenticado

```text
docs/images/dashboard-authenticated.png
```

### CRUD de Alertas

```text
docs/images/dashboard-alerts.png
```

## Endpoints Principales

### Auth

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `POST` | `/auth/register` | Crear usuario |
| `POST` | `/auth/login` | Obtener JWT |
| `GET` | `/auth/me` | Obtener usuario autenticado |

### Alertas

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `GET` | `/alertas/` | Listar alertas del usuario |
| `POST` | `/alertas/` | Crear alerta |
| `GET` | `/alertas/{alerta_id}` | Ver detalle de alerta |
| `PUT` | `/alertas/{alerta_id}` | Editar alerta |
| `PATCH` | `/alertas/{alerta_id}/activar` | Activar alerta |
| `PATCH` | `/alertas/{alerta_id}/desactivar` | Desactivar alerta |
| `DELETE` | `/alertas/{alerta_id}` | Eliminar alerta |

### Ofertas

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `GET` | `/ofertas/` | Listar ofertas |
| `POST` | `/ofertas/` | Crear oferta |
| `GET` | `/ofertas/{oferta_id}` | Ver detalle de oferta |
| `PATCH` | `/ofertas/{oferta_id}/estado` | Actualizar estado |

### Scraper

| Metodo | Endpoint | Descripcion |
|---|---|---|
| `POST` | `/scraper/sync` | Sincronizacion manual actual |

La documentacion interactiva completa esta en:

```text
http://localhost:8000/docs
```

## Estado Actual del Desarrollo

Implementado:

- Docker Compose funcional.
- API FastAPI funcional.
- PostgreSQL funcional.
- Autenticacion JWT.
- Modelos base SaaS.
- CRUD completo de alertas.
- Dashboard autenticado.
- Preparacion de InfoJobs con variables de entorno y datos mock.
- Tests automatizados basicos.

Pendiente:

- Scheduler real.
- Integracion real con InfoJobs.
- Notificaciones por Telegram.
- Notificaciones por email.
- Flujo completo de ofertas por usuario.
- Mejoras visuales del dashboard.
- Documentacion con capturas reales.

## Roadmap

- [x] Configuracion Docker Compose.
- [x] API FastAPI.
- [x] PostgreSQL.
- [x] Auth JWT.
- [x] Modelo `User`.
- [x] Modelo `Alert`.
- [x] CRUD completo de alertas.
- [x] Dashboard autenticado con Streamlit.
- [x] Preparacion de InfoJobs sin credenciales reales.
- [ ] Scheduler para ejecuciones automaticas.
- [ ] Integracion real con InfoJobs.
- [ ] Telegram.
- [ ] Email.
- [ ] Gestion completa de ofertas por usuario.
- [ ] Historial completo de notificaciones.
- [ ] Deploy.

## Tests

Ejecutar tests:

```bash
.venv/bin/python -m pytest --ignore-glob='*-JESUSPC*'
```

Tambien puede usarse:

```bash
pytest
```

Los tests actuales cubren:

- Inicio basico de la API.
- Auth: registro, login y usuario autenticado.
- Rutas protegidas.
- CRUD de ofertas existente.
- CRUD de alertas.
- Aislamiento de alertas por usuario.
- Scrapers con mocks.
- Sincronizacion mock.

## Licencia

Distribuido bajo licencia MIT. Consulta el archivo `LICENSE` si esta disponible en el repositorio.

## Autor

**Jesus Granados y Oliver Lugo**

- GitHub: [Ciscojes](https://github.com/Ciscojes)
