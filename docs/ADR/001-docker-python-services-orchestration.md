30-03-2026 11:53

Status: Concluded

Tags: [[Infrastructure]] [[Docker]]

ID: 001

# Docker + Python Services Orchestration

# 1. Business context

The system needs to process purchase requisition emails through n8n, which calls a Python/FastAPI service for attachment processing. The original project had structural issues preventing correct container communication, including mismatched module paths, missing dependency management, and no health verification between services.

# 2. Problems identified

| # | Problem | Impact |
|---|---------|--------|
| 1 | Dockerfile copied entire project (`COPY . .`) but compose volume mounted only `./python_scripts:/app` | Inconsistent container structure — code inside container didn't reflect mounted structure |
| 2 | CMD in Dockerfile vs command in compose diverged — Dockerfile: `python_scripts.app.main:app`, compose: `python_scripts.main:app` | Only one path worked; the other generated `ModuleNotFoundError` |
| 3 | Volume mounted `./python_scripts` at `/app` but uvicorn referenced `python_scripts.main` | Inside `/app` there was no `python_scripts` subdirectory |
| 4 | No `requirements.txt` — dependencies installed inline in Dockerfile | No version lock, non-reproducible builds |
| 5 | No `__init__.py` in Python packages | Relative imports could fail |
| 6 | Endpoint `/attachmentProcessingService` untyped | Parameter `file` didn't use `UploadFile` from FastAPI — couldn't receive multipart/form-data correctly |
| 7 | No explicit Docker network | Containers depended on default network without isolation |
| 8 | No healthcheck | No way to detect if Python service was ready before n8n made requests |
| 9 | LLM Schema was a `.py` file with raw JSON | Should be a Pydantic model |

# 3. Technical decisions

## 3.1 Project restructure: `python_scripts/` → `python_service/`

Renamed and restructured the Python project to follow FastAPI conventions with clear separation of responsibilities: `api/routes/`, `domain/`, `services/`, and `tests/`.

**Rationale:** The flat structure made it impossible to correctly resolve module paths inside the Docker container. The new layout follows standard FastAPI project conventions and ensures `uvicorn app.main:app` works consistently in both Dockerfile CMD and compose command.

## 3.2 Dockerfile layer caching

Dependencies are installed before copying application code (`COPY requirements.txt` → `RUN pip install` → `COPY ./app`). This ensures Docker layer cache is used for dependencies, making rebuilds fast when only code changes.

## 3.3 Hot reload via volume mount

The compose volume mounts only `./python_service/app:/app/app` (the code directory), not the entire project. Combined with `uvicorn --reload --reload-dir /app/app`, this provides instant hot reload during development without interfering with installed dependencies.

## 3.4 Explicit Docker network

Created `app-network` (bridge driver) for container isolation. All services communicate through this network, with the Python service accessible at `http://python:8000` from n8n.

## 3.5 Health-first dependency chain

Python service exposes `GET /health` returning `{"status": "healthy"}`. Docker compose uses `depends_on` with `condition: service_healthy` so n8n only starts after Python is confirmed ready.

## 3.6 Image version pinning

| Image | Version | Rationale |
|-------|---------|-----------|
| `python` | `3.13-slim` | Stable LTS. Python 3.14 was pre-release with CVE-2026-2297 |
| `n8nio/n8n` | `1.123.27` | Last stable 1.x. Version 1.76.1 was incompatible with existing database schema (`roleSlug` vs `role` column). CVEs in 1.65–1.120.4 patched since 1.121.0 |
| `cloudflare/cloudflared` | `latest` | Temporary tunnels via trycloudflared for MVP — no persistent tunnel config needed |

## 3.7 Credential extraction

Moved `N8N_BASIC_AUTH_USER`, `N8N_BASIC_AUTH_PASSWORD`, and `N8N_ENCRYPTION_KEY` from hardcoded docker-compose values to `.env` file (excluded from git via `.gitignore`).

## 3.8 Pydantic schema migration

Converted `llmClassificationOutput.py` (raw JSON file) to a proper Pydantic `BaseModel` in `llm_classification.py`, enabling runtime validation and type safety.

# 4. Trade-offs

**PROS**
- Reproducible builds with pinned dependency versions
- Fast development cycle with hot reload
- Clear separation of concerns (routes, services, domain)
- Service health verification prevents cascading failures
- Credentials extracted from version control

**CONS**
- Pinned versions require manual update tracking (mitigated by CHANGELOG policy)
- Hot reload volume mount means container filesystem diverges slightly from production image
- `cloudflared:latest` violates pinning rule (accepted for MVP temporary tunnels)

# 5. n8n version migration note

The existing `n8n_data/database.sqlite` was created by n8n ≥1.110, where migration `RemoveOldRoleColumn` renamed `role` → `roleSlug`. Pinning to 1.76.1 (pre-migration) caused `SQLITE_ERROR: no such column USER.role`. Solution: pin to 1.123.27 (last stable 1.x with all security patches and compatible schema).

# References

- CVE-2026-2297: CPython Logging Bypass in Legacy .pyc File Handling
- n8n GitHub Issue: RemoveOldRoleColumn migration (versions 1.110–1.115)
- n8n Release 1.123.27: Last 1.x maintenance release (2026-03-25)
