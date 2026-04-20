# AI Tools Compare

A full-stack web application for comparing AI model pricing, context windows, and capabilities across major providers (OpenAI, Anthropic, Google, DeepSeek).

Live demo: [ai-compare.duckdns.org](https://ai-compare.duckdns.org)
API docs: [ai-compare-api.duckdns.org/api/v1/docs](https://ai-compare-api.duckdns.org/api/v1/docs)

## Tech Stack

**Frontend**
- Astro 5 (static site generation with island architecture)
- React 19 (interactive components)
- TypeScript (strict mode)

**Backend**
- Python 3.12
- FastAPI (async REST API)
- SQLAlchemy 2.0 (async ORM)
- Alembic (database migrations)
- Pydantic v2 (request/response validation)

**Infrastructure**
- PostgreSQL 17
- Docker + Docker Compose (multi-container orchestration)
- Nginx Proxy Manager (reverse proxy + Let's Encrypt SSL)
- Deployed on Oracle Cloud ARM server

## Architecture
Client (HTTPS) │ ▼ Nginx Proxy Manager (SSL termination, reverse proxy) │ ├──► aitc-frontend (Astro dev server / SSG output, port 4321) └──► aitc-backend (FastAPI + Uvicorn, port 8000) │ ▼ aitc-postgres (PostgreSQL 17)

All services run as isolated Docker containers on a shared Docker network. The frontend is decoupled from the backend via a REST API, allowing independent scaling and deployment.
## Features
- **Real-time model comparison table** — Sortable by price, context window, or provider
- **Provider filtering** — Instantly filter by OpenAI, Anthropic, Google, or DeepSeek
- **Responsive UI** — Dark theme, mobile-friendly
- **Swagger/OpenAPI docs** — Auto-generated interactive API documentation
- **Type-safe end-to-end** — TypeScript on frontend, Pydantic on backend
## Local Development
### Prerequisites
- Docker & Docker Compose
- Node.js 22+ (if running frontend outside container)
- Python 3.12+ with `uv` (if running backend outside container)
### Setup

```bash
git clone https://github.com/Pengfei-Kou/ai-tools-compare.git
cd ai-tools-compare
docker compose up -d --build
Services will be available at:

Frontend: http://localhost:4321
Backend API: http://localhost:8000/api/v1/docs
Postgres: localhost:5433
```

### Database Migrations
```
docker compose exec backend uv run alembic revision --autogenerate -m "describe change"
docker compose exec backend uv run alembic upgrade head
```
### Seed Data
`docker compose exec backend uv run python -m scripts.seed_models`

## Project Structure
ai-tools-compare/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/                # Route handlers
│   │   ├── core/               # Config, database, security
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response models
│   │   └── services/           # Business logic layer
│   ├── alembic/                # DB migration scripts
│   ├── scripts/                # Seed/maintenance scripts
│   ├── Dockerfile
│   ├── main.py                 # App entry point
│   └── pyproject.toml
├── frontend/                   # Astro + React frontend
│   ├── src/
│   │   ├── components/         # React interactive components
│   │   ├── layouts/            # Astro page layouts
│   │   ├── pages/              # Astro routes
│   │   ├── lib/                # API client
│   │   ├── styles/             # Global CSS
│   │   └── types/              # TypeScript types
│   ├── Dockerfile
│   ├── astro.config.mjs
│   └── package.json
└── docker-compose.yml          # Multi-service orchestration
## API Overview

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| GET    | /health             | Health check              |
| GET    | /api/v1/models/     | List all active AI models |
| GET    | /api/v1/models/{id} | Get a specific model      |
| POST   | /api/v1/models/     | Create a new model        |

Full interactive documentation available at /api/v1/docs.


## Roadmap

- [ ] Price calculator (estimate monthly cost by usage)

- [ ] Historical price tracking and trend charts

- [ ] Blog section with MDX articles

- [ ] Automated price scraper for provider APIs

- [ ] pytest + Vitest test coverage

- [ ] GitHub Actions CI/CD pipeline

## License
MIT
