<div align="center">

```
     ██╗ ██████╗ ██████╗     ██████╗  █████╗ ██████╗  █████╗ ██████╗ 
     ██║██╔═══██╗██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔══██╗
     ██║██║   ██║██████╔╝    ██████╔╝███████║██║  ██║███████║██████╔╝
██   ██║██║   ██║██╔══██╗    ██╔══██╗██╔══██║██║  ██║██╔══██║██╔══██╗
╚█████╔╝╚██████╔╝██████╔╝    ██║  ██║██║  ██║██████╔╝██║  ██║██║  ██║
 ╚════╝  ╚═════╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
```

**Radar de ofertas de empleo — Infojobs API + filtros personalizados + alertas por Telegram** 🎯

![Python](https://img.shields.io/badge/Python-3.11+-00FF41?style=for-the-badge&logo=python&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-00FF41?style=for-the-badge&logo=fastapi&logoColor=black)
![Infojobs](https://img.shields.io/badge/Infojobs-API%20Oficial-00FF41?style=for-the-badge&logoColor=black)
![Telegram](https://img.shields.io/badge/Telegram-Bot-00FF41?style=for-the-badge&logo=telegram&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-00FF41?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-En%20Desarrollo-yellow?style=for-the-badge)

</div>

---

## `$ whoami`

**jobradar-py** es una herramienta que centraliza y filtra ofertas de empleo usando la **API oficial de Infojobs**. Guarda las ofertas en una base de datos, permite buscarlas con filtros avanzados y te avisa por **Telegram** cuando aparece algo que encaja con tu perfil.

> Porque tu próximo trabajo no debería encontrarte a ti buscando manualmente.

---

## `$ cat features.txt`

- 📡 **Infojobs API oficial** — sin scraping, sin bloqueos, datos limpios y legales
- 🔍 **Filtros avanzados** — tecnología, ciudad, modalidad (remoto / presencial / híbrido), salario
- ⏱️ **Actualización automática** — nuevas ofertas cada X horas con APScheduler
- 🔔 **Alertas por Telegram** — aviso instantáneo cuando aparece una oferta que encaja con tu perfil
- 📋 **Panel de seguimiento** — marca ofertas como `aplicado`, `guardado` o `descartado`
- 🌐 **API REST** — endpoints documentados con Swagger UI en `/docs`
- 🖥️ **Dashboard web** — interfaz visual para explorar y gestionar tus ofertas

---

## `$ ls tech-stack/`

```
backend/
├── FastAPI          → API REST + documentación automática con Swagger
├── SQLAlchemy       → ORM para gestión de base de datos
├── SQLite           → almacenamiento local (PostgreSQL en producción)
├── APScheduler      → actualización automática de ofertas
├── Requests         → consumo de la API de Infojobs
└── python-telegram-bot → alertas en tiempo real por Telegram

frontend/
└── Streamlit        → dashboard para búsqueda y seguimiento de ofertas
```

---

## `$ tree jobradar-py/`

```
jobradar-py/
│
├── app/
│   ├── main.py                  # Punto de entrada FastAPI
│   ├── database.py              # Configuración SQLAlchemy
│   ├── models.py                # Modelos de base de datos
│   ├── schemas.py               # Schemas Pydantic
│   │
│   ├── scraper/
│   │   ├── infojobs.py          # Consumo de la API oficial de Infojobs
│   │   └── indeed.py            # Scraper adicional (Indeed España)
│   │
│   ├── routers/
│   │   ├── ofertas.py           # CRUD de ofertas
│   │   └── alertas.py           # Gestión de alertas personalizadas
│   │
│   └── services/
│       ├── scheduler.py         # Tareas periódicas con APScheduler
│       └── telegram.py          # Notificaciones vía Telegram Bot
│
├── dashboard/
│   ├── app.py                   # App Streamlit principal
│   └── components/              # Componentes reutilizables del dashboard
│
├── tests/
│   ├── test_api.py
│   └── test_scraper.py
│
├── .env.example
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## `$ pip install -r requirements.txt && ./setup.sh`

### 1. Clona el repositorio

```bash
git clone https://github.com/OLIVER26GOLDEN/jobradar-py.git
cd jobradar-py
```

### 2. Crea el entorno virtual e instala dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 3. Configura las variables de entorno

```bash
cp .env.example .env
```

```env
# .env
DATABASE_URL=sqlite:///./jobradar.db

# Infojobs API
INFOJOBS_CLIENT_ID=tu_client_id
INFOJOBS_CLIENT_SECRET=tu_client_secret

# Telegram Bot
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id

# Scheduler
SCRAPER_INTERVAL_HOURS=6
```

> Consigue tus credenciales de Infojobs en [developer.infojobs.net](https://developer.infojobs.net)

### 4. Arranca el servidor

```bash
uvicorn app.main:app --reload
```

### 5. Abre el dashboard

```bash
streamlit run dashboard/app.py
```

---

## `$ curl http://localhost:8000/docs`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/ofertas` | Lista ofertas con filtros opcionales |
| `GET` | `/ofertas/{id}` | Detalle de una oferta |
| `PATCH` | `/ofertas/{id}/estado` | Actualiza estado (aplicado, guardado...) |
| `POST` | `/alertas` | Crea una alerta personalizada |
| `GET` | `/alertas` | Lista tus alertas activas |
| `DELETE` | `/alertas/{id}` | Elimina una alerta |
| `POST` | `/scraper/sync` | Sincroniza manualmente con Infojobs API |

Documentación interactiva completa en `http://localhost:8000/docs`

---

## `$ cat roadmap.md`

- [x] Diseño de arquitectura y estructura del proyecto
- [ ] Integración con la API oficial de Infojobs
- [ ] Modelos de base de datos (SQLAlchemy)
- [ ] API REST con FastAPI
- [ ] Sistema de alertas por Telegram
- [ ] Scheduler de actualización automática
- [ ] Dashboard con Streamlit
- [ ] Scraper adicional (Indeed España)
- [ ] Tests unitarios
- [ ] Dockerización del proyecto
- [ ] Soporte para PostgreSQL en producción

---

## `$ git log --authors`

| Dev | GitHub | Área |
|-----|--------|------|
| Oliver Lugo | [@OLIVER26GOLDEN](https://github.com/OLIVER26GOLDEN) | Backend · API · Base de datos · Servicios |
| Tu amigo | [@usuario](https://github.com/usuario) | Dashboard · Filtros · Tests |

---

## `$ cat LICENSE`

MIT License — úsalo, modifícalo, mejóralo. Si te resulta útil, dale una ⭐

---

<div align="center">

*Built with 🖤 and too much caffeine*

</div>
