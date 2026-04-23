# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-30

### Added
- **Python service structure** (`python_service/`): FastAPI app factory with modular routing (`api/routes/`), domain layer (`domain/enums/`, `domain/schemas/`), and service layer (`services/`)
- **Attachment processing endpoint** `POST /attachmentProcessingService`: receives `multipart/form-data` with typed `UploadFile` parameter
- **Health check endpoint** `GET /health`: returns `{"status": "healthy"}` for Docker healthcheck
- **Pydantic schema** `LLMClassificationOutput`: typed model replacing raw JSON schema file
- **PurchaseType enum** (`str, Enum`): SPOT, PLANNED, CONTRACT, SERVICE, STO
- **Docker compose orchestration**: explicit `app-network`, healthcheck-based dependency chain (`n8n` depends on `python` healthy)
- **Dockerfile** with layer caching strategy: dependencies installed before code copy
- **Hot reload** in development: volume mounts `./python_service/app` with `uvicorn --reload`
- **Dependency management**: `requirements.txt` and `requirements-dev.txt` with pinned versions
- **Credential extraction**: `.env` file for sensitive n8n variables, `.env.example` as template
- **Testing structure**: `conftest.py` with httpx `AsyncClient` fixture, unit and integration tests
- **ADR 001**: Docker + Python services orchestration decisions
- **ADR 002**: Multi-format attachment processing strategy

### Changed
- **n8n image** pinned from `latest` to `1.123.27` (last stable 1.x, compatible with existing database schema using `roleSlug`)
- **Python image** from `3.14-slim` (pre-release) to `3.13-slim` (stable LTS)
- **Project directory** renamed from `python_scripts/` to `python_service/`

### Security
- Removed hardcoded credentials from `docker-compose.yml` (moved to `.env`)
- `.gitignore` updated to exclude `.env`, `n8n_data/`, `__pycache__/`
- Python 3.14 avoided due to CVE-2026-2297
- n8n 1.123.27 includes patches for CVEs in versions 1.65–1.120.4

### Removed
- Root-level `Dockerfile` (replaced by `python_service/Dockerfile`)
- Old `python_scripts/` directory structure
- Raw JSON schema file `llmClassificationOutput.py`
