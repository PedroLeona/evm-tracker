# Plan de Gitflow

El historial del repositorio es parte de la entrega, así que debe reflejar tu trabajo real: haz cada commit **mientras revisas, entiendes y ajustas** cada módulo, no todo de golpe al final.

## Estructura de ramas

- `main`: producción. Solo recibe el merge de `release/*`.
- `develop`: integración. Recibe cada `feature/*` mediante Pull Request.
- `feature/*`: una por funcionalidad.
- `release/1.0.0`: estabilización antes del merge final a `main`.

## Preparación

```bash
cd evm-tracker
git init -b main
git add .gitignore README.md
git commit -m "Add project README and gitignore"
git branch develop && git switch develop
```

Crea el repo vacío en GitHub, conecta el remoto (`git remote add origin ...`) y sube `main` y `develop`.

## Features sugeridas (orden y commits)

| Rama | Contenido | Commits de ejemplo (imperativo) |
|---|---|---|
| `feature/database-schema` | `db/` | `Add PostgreSQL schema with integrity constraints`<br>`Add demo seed data with hand-computed results` |
| `feature/evm-domain` | `backend/app/domain/`, `constants.py`, tests unitarios del cálculo | `Add EVM calculation domain with PV, EV, CV, SV`<br>`Add CPI, SPI, EAC and VAC with undefined-index handling`<br>`Add unit tests for EVM edge cases` |
| `feature/project-api` | modelos, repositorios, servicios y routers de proyectos | `Add project and activity models`<br>`Add project service and CRUD endpoints` |
| `feature/activity-api` | servicios y routers de actividades, `mappers.py` | `Add activity service with EVM metrics in responses`<br>`Add integration tests for activity endpoints` |
| `feature/evm-report-endpoint` | `/projects/{id}/evm` | `Add consolidated EVM report endpoint` |
| `feature/openapi-docs` | descripciones, `responses`, `/api-docs` | `Document error responses in OpenAPI` |
| `feature/frontend-dashboard` | `frontend/src` | `Add API client and data hooks`<br>`Add KPI panel with CPI and SPI traffic lights`<br>`Add PV, EV and AC chart per activity`<br>`Add activity table and form` |
| `feature/docker-setup` | Dockerfiles, `docker-compose.yml` | `Add Docker Compose setup for db, backend and frontend` |
| `feature/lint-config` | `pyproject.toml` (ruff), ESLint | `Configure ruff and ESLint rules` |

## Flujo de cada feature

```bash
git switch develop
git switch -c feature/evm-domain
# ... trabaja, prueba, haz commits pequeños ...
git push -u origin feature/evm-domain
# Abre un Pull Request hacia develop en GitHub, revisa el diff y haz merge.
git switch develop && git pull
```

## Release

```bash
git switch develop && git pull
git switch -c release/1.0.0
# Ajustes finales: versión, README, verificación de tests y linter
git commit -m "Prepare release 1.0.0"
git push -u origin release/1.0.0
# PR release/1.0.0 -> main; tras el merge, etiqueta y sincroniza develop:
git switch main && git pull
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
git switch develop && git merge main && git push
```

## Reglas de commit

- Imperativo y descriptivo: `Fix CPI edge case when AC is zero`.
- Evita `fix`, `cambios`, `wip`.
- Un commit = un cambio con sentido; los tests van junto al código que prueban.
