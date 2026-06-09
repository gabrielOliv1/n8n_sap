# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-05-01

### Added
- **Email Processing Service** (`POST /emailProcessingService`): new endpoint accepting `application/json` array produced by n8n (M2).
- **Domain schemas** (`email_payload.py`, `email_response.py`): Pydantic models for inbound n8n payload and outbound cleaned response.
- **Service layer** (`email_processor.py`): orchestrates field cleaning, base64 decode, and PDF text preview extraction (first 5 000 chars).
- **Text cleaner** (`text_cleaner.py`): extensible footer removal pipeline with structured logging of every removed fragment.
- **ADR-004**: Email Processing Service architectural decisions.
- **Tests**: 35 new tests (unit + integration) covering schemas, text cleaner, processor helpers, and HTTP endpoint contract.

### Changed
- **`main.py`**: registered email router; updated app version to `0.4.0`.
- **`main.py`**: added Google-style docstring to `create_app()`.

### Deprecated
- **`POST /attachmentProcessingService`**: kept active during n8n transition period; will be removed in M3.

### Notes
- **n8n workflow change required (manual)**: Update the HTTP Request node URL from `http://python:8000/attachmentProcessingService` to `http://python:8000/emailProcessingService`. Change content-type from `multipart/form-data` to `application/json`.

## [0.3.0] - 2026-04-29

### Added
- **CI/CD pipeline**: integrated GitHub Actions pipeline (M1).
- **Tests**: added validation testing for the `purchase type` schema.

### Changed
- **Dependencies**: updated project dependency versions.

### Fixed
- **Docker image naming**: corrected Docker image nomenclature across all instances.
- **Trivy workflow**: fixed vulnerability scanning by installing Trivy directly in the container.
- **Code formatting**: resolved `black` and `ruff` checking issues.

## [0.2.0] - 2026-04-23

### Added
- **CI workflow** (`.github/workflows/ci.yml`): 3 parallel jobs on every PR to `master` — code quality (black, ruff, mypy), tests (pytest + coverage ≥80%), security (pip-audit, trivy, gitleaks)
- **Release workflow** (`.github/workflows/release.yml`): automatic git tag + GitHub Release from CHANGELOG.md version on merge to `master`
- **mypy configuration** (`python_service/mypy.ini`): type checking with `ignore_missing_imports` for third-party libraries without stubs
- **CI/CD documentation** (`docs/CI_CD.md`): pipeline strategy, local commands, branch protection setup, troubleshooting
- **ADR 003**: GitHub Actions CI/CD pipeline decisions

### Changed
- **requirements-dev.txt**: added `pytest-cov==6.1.1`, `black==25.1.0`, `ruff==0.11.8`, `mypy==1.15.0`, `pip-audit==2.9.0`
- **SPEC.md**: updated milestone M1 status to CONCLUDED, removed CI/CD "not implemented" note

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
