# EVM Tracker

Aplicación fullstack para gestionar proyectos y actividades y calcular automáticamente los indicadores de **Valor Ganado (Earned Value Management)** por actividad y consolidados por proyecto.

- **Backend:** Python 3.12 · FastAPI · SQLAlchemy 2 · PostgreSQL
- **Frontend:** React 18 · Vite · Recharts
- **Calidad:** pytest (cobertura ≥ 80 %), ruff, ESLint, OpenAPI en `/api-docs`

## Ejecutar con Docker (recomendado)

```bash
docker compose up --build
```

| Servicio | URL |
|---|---|
| Dashboard | http://localhost:3000 |
| API + Swagger UI | http://localhost:8000/api-docs |
| ReDoc | http://localhost:8000/api-redoc |

La base de datos se inicializa sola con los scripts de `db/`:

- `db/01_init.sql`: esquema (tablas, restricciones, índices).
- `db/02_seed.sql`: proyecto demo con 3 actividades. Borra este archivo antes del primer arranque si no lo quieres.

Para reiniciar la base desde cero: `docker compose down -v`.

## Ejecutar sin Docker

Requisitos: Python 3.12+, Node 20+, PostgreSQL.

```bash
# 1. Base de datos
createdb evm
psql evm -f db/01_init.sql
psql evm -f db/02_seed.sql        # opcional

# 2. Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
export DATABASE_URL=postgresql+psycopg://USER:PASS@localhost:5432/evm
uvicorn app.main:app --reload     # http://localhost:8000/api-docs

# 3. Frontend (otra terminal)
cd frontend
npm install
npm run dev                       # http://localhost:5173 (proxy a :8000)
```

## Pruebas y calidad

```bash
cd backend
pytest --cov                      # falla si la cobertura baja de 80 %
ruff check .                      # linter (config en pyproject.toml)

cd ../frontend
npm run lint
```

Los tests usan SQLite en memoria, por lo que no necesitan PostgreSQL.

## Fórmulas

| Indicador | Fórmula |
|---|---|
| PV | % planificado × BAC |
| EV | % completado × BAC |
| CV | EV − AC |
| SV | EV − PV |
| CPI | EV / AC |
| SPI | EV / PV |
| EAC | BAC / CPI |
| VAC | BAC − EAC |

### Decisiones de cálculo

- **Consolidado por proyecto:** se suman BAC, PV, EV y AC de las actividades y *después* se calculan los índices. Nunca se promedian CPI/SPI (daría más peso a actividades pequeñas).
- **Índice indefinido → `null`:** si AC = 0 el CPI es `null`; si PV = 0 el SPI es `null`; si CPI es `null` o 0, EAC y VAC son `null`. Se devuelve `null` (y estado `UNDEFINED`) para no confundir "sin datos" con "va mal" ni con "va perfecto".
- **Dinero con `Decimal`:** sin errores de punto flotante. Los valores se redondean (half-up) solo al construir la respuesta: dinero a 2 decimales, índices a 4.
- **Proyecto sin actividades:** totales en 0 e índices `null`.

## API

Documentación interactiva completa en `/api-docs`.

| Método | Ruta | Descripción |
|---|---|---|
| GET / POST | `/api/projects` | Listar / crear proyectos |
| GET / PUT / DELETE | `/api/projects/{id}` | Consultar / reemplazar / eliminar |
| GET | `/api/projects/{id}/evm` | Reporte EVM: consolidado + actividades |
| GET / POST | `/api/projects/{id}/activities` | Listar / crear actividades |
| GET / PUT / DELETE | `/api/activities/{id}` | Consultar / reemplazar / eliminar |
| GET | `/health` | Liveness |

Códigos de error: `404` recurso inexistente (`{"detail": "..."}`), `422` validación (BAC > 0, porcentajes 0–100, AC ≥ 0).

## Arquitectura

```
backend/app/
├── routers/       # HTTP: solo traducen request/response
├── services/      # casos de uso (proyectos, actividades, puente a EVM)
├── domain/        # cálculo EVM puro, sin framework ni I/O
├── repositories.py# acceso a datos
├── schemas.py     # contrato de la API (Pydantic → OpenAPI)
└── models.py      # entidades SQLAlchemy
```

La lógica de negocio no vive en los controladores. `domain/` no conoce FastAPI ni la base de datos, por eso se prueba sin mocks.

## Documentos del proceso

- [`AI_PROCESS.md`](AI_PROCESS.md): proceso de trabajo con IA.
- [`docs/EVM_STUDY_GUIDE.md`](docs/EVM_STUDY_GUIDE.md): guía de estudio del Valor Ganado.
- [`docs/GITFLOW_PLAN.md`](docs/GITFLOW_PLAN.md): ramas, PRs y mensajes de commit.

## Architecture

The application follows a layered architecture:

- **Frontend:** React application responsible for the user interface.
- **API:** FastAPI endpoints that handle HTTP requests.
- **Services:** Coordinate business operations.
- **Repositories:** Manage database persistence.
- **Domain:** Contains the Earned Value Management calculations.
- **Database:** PostgreSQL stores projects and activities.