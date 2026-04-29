`Instructions: Read this file completely before any action. After reading it, consult plan.md to the actual milestone task. Do not create any structure or behavior that is not described here - if anything is missing, raise a question before taking any action.`
# 1. PROJECT CONTEXT:

Domain: Corporative purchase automation by email

What the system do: n8n reads the email and the attachments -> run business rules -> classify the document through LLM response -> LLM suggests a workflow.

---
# 2. STACK

- Orchestrator: n8n (container `n8nio/n8n:1.123.27`)
- Processing service: Python 3.13/FastAPI (container Python)
- Tunnel: Cloudflare (`cloudflare/cloudflared:2025.10.0`)
- Infrastructure: Isolated network with docker compose app-network

Integration principle: n8n calls the Python service by internal HTTP (http://python:8000). Python service never know n8n - the communication starts in the orchestrator side

---
# 3. FILE STRUCTURE 

/
├── SPEC.md                          ← This file (layer 1 — permanent)
├── plan.md                          ← actual milestone task (layer 2 — temporary)
├── CHANGELOG.md                     ← release history (agent update at every merge)
├── .env                             ← credentials (never commited)
├── .env.example                     ← template
├── .gitignore
├── docker-compose.yml
├──workspace.json       ← JSON describing the relationship between the entities (architecture view)
├── docs/
│   ├── ADR/                         ← Architectural Decision Records
│   │   └── NNN-small-title.md      ← NNN format: 001, 002...
│   ├── TESTING_STRATEGY.md          ← detailed testing strategy
│   └── CI_CD.md                     ← pipeline strategy
└── python_service/
    ├── app/
    │   ├── main.py
    │   ├── api/
    │   │   └── routes/
    │   │       ├── attachment.py
    │   │       └── health.py
    │   ├── domain/
    │   │   ├── enums/
    │   │   │   └── purchase_type.py
    │   │   └── schemas/
    │   │       └── llm_classification.py
    │   └── services/
    │       └── attachment_processor.py
    ├── tests/
    │   ├── conftest.py
    │   ├── unit/
    │   │   └── test_attachment_processor.py
    │   ├── integration/
    │   │   └── test_attachment_endpoint.py
    │   └── regression/
    │       └── .gitkeep
    ├── requirements.txt
    ├── requirements-dev.txt
    └── Dockerfile

Rule: When creating a new file, check if it belongs to any categories above. If not, suggests the creation of the structure before creating the file

---
# 4. SDLC

The agent will follow this cycle without exceptions

SPEC.md -> plan.md -> Testing stage -> Implementation -> Refactoring -> Release -> Changelog + ADR

## 4.1 Mandatory phase by tasks

### Phase 1 - Context reading before any code
- Read SPEC.md
- Read plan.md to understand the milestone task
- Read CHANGELOG.md to understand the actual state
- Read relevants ADRs in `docs/ADR` if the task involves a decision already taken

### Phase 2 - Testing first (TDD mandatory)
- None line of production code must be written before correspondent testing exists
- The tests will fail before the implementation (red)
- The implementation exists to make the tests successfull (green)
- Refactor happens with the successfull testing (green)
- After refactoring, regression testing must be performed

### Phase 3 - Implementation
- Follow code conventions from topic 6
- Every function must be documented at moment creation (topic 7)
- Atomic commits: one responsibility = one commit

### Phase 4 - Refactor
- If any function exceeds 30 lines of code -> extract
- If any module exceeds 200 lines -> separation
- Check duplicates: if a pattern is found 3 times -> abstract
- Folllow the DRY

### Phase 4 - Release
- Changelog.md updated always
- If any architecure decision was taken -> create ADR in `docs/ADR`
- Check if plan.md were completely executed -> conclude milestone

### 4.2 Release sizes
- Each release implements one component from plan.md
- Never mix refactor with new feature in the same commit
- PRs with > 400 lines must have an explicit justification

---
# 5 TESTING STRATEGY
## 5.1 Principles
- TDD is mandatory
- Testing share: more unit testing, less integration tests and regression testing for fixed bugs
- Test ratio 1:1 - 1 line of testing for line of code
- Tests should not depend on execution order, without shared states among tests

## 5.2 Responsabilities
### Unit tests (tests/unit)
- Test only one function or isolated class
- Mocked database, HTTP requests and files
- Must run in < 1 sec each
- Nomenclature: `test_function_scenario_expecte_result`
- Ex: `test_process_file_with_pdf_returns_extracted_text`

### Integration tests (tests/integration)
- Test HTTP endpoint entirely using `http.AsyncClient` with `ASGITransport`
- Without real containeres - FastAPI instancied in memory
- Cover the API contract: status codes, response schema and headers.

### Regression tests (tests/regression)
- Created only when a bug is fixed
- Test reproduces the bug before the correction, and pass after
- Never removed, they are the memory of the system

## 5.3 Fixtures and factories

Every shared fixture lives in `tests/conftest.py`. Specific fixtures from a test module stays in the test file.

Pattern:
```
import pytest
from pathlib import Path

@pytest.fixture
def sample_pdf_bytes() -> bytes:
    """Retorna bytes de um PDF mínimo válido para testes."""
    return (Path(__file__).parent / "fixtures" / "sample.pdf").read_bytes()

@pytest.fixture
def sample_docx_bytes() -> bytes:
    """Retorna bytes de um DOCX mínimo válido para testes."""
    return (Path(__file__).parent / "fixtures" / "sample.docx").read_bytes()
```

## 5.4 Tests commands
```
# Run all tests
cd python_service
pytest tests/ -v --tb=short

# Run with coverage
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80

# Run unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run specific test
pytest tests/unit/test_attachment_processor.py::test_process_file_with_pdf_returns_extracted_text -v
```

## 5.5 Edge cases mandatory for each endpoint

For every new endpoint, the following scenarios are mandatory before the implementation


| CATEGORY     | SCENARIO                              | EXPECTED HTTP                |
| ------------ | ------------------------------------- | ---------------------------- |
| Happy path   | Valid input                           | 200                          |
| Validation   | Without payload/mandatory field empty | 422                          |
| Invalid type | Extension not supported               | 400                          |
| Size         | File above size limit (10MB)          | 413                          |
| Corruption   | Invalid bytes                         | 400                          |
| Null         | File with 0 bytes                     | 400                          |
| Health       | GET /health                           | 200 + { "status": "health" } |

---
# 6. Code convention
## 6.1 Python
- `setting.json` runs Ruff lint and formatter
-  `black` format for python
- I/O Functions must be async
- Exceptions: never `raise Exception(...)`, use HTTPException

## 6.2 Docker
- Images always with pinned versions - never latest
- Critical environmments variables always by env file
- All services must have a healthceck before being reference in `depends_on`
- Hot reload volumn build the code dir /app, never the entire project


## 6.3 Pinned versions

Rule: when updating any version of any component, document the why in the CHANGELOG.md and check the known CVEs before updating.

---
# 7. Documentation

## 7.1 Docstrings

Every public function uses docstring in google style format

```
async def process_file(file: UploadFile) -> dict:
    """Extrai o conteúdo textual de um anexo enviado via upload.

    Args:
        file: Arquivo recebido via multipart/form-data. Extensões suportadas:
              .pdf, .docx, .xlsx, .csv, .txt

    Returns:
        Dicionário com chave 'content' contendo o texto extraído.

    Raises:
        HTTPException 400: Extensão não suportada, arquivo corrompido ou vazio.
        HTTPException 413: Arquivo excede MAX_FILE_SIZE_MB (10 MB).
    """
```

## 7.2 Documentation rules
- Docstring in the same implementation commit always;
- Constants with values non-explicit must have a comment explaining the value origin

## 7.3 ADR

Every decision with architecture impact must generate an ADR in `docs/ADR`, with format [[Template ADR]] 

---
# 8. CI/CD

More details on [docs/CI_CD.md](docs/CI_CD.md).

## 8.1 Mandatory checks in every PR

Follow the below sequence:

| CHECK                         | TOOL                       | FAIL BLOCK MERGE? |
| ----------------------------- | -------------------------- | ----------------- |
| Formats                       | black --check              | Y                 |
| Linting                       | ruff check                 | Y                 |
| Type check                    | mypy                       | Y                 |
| Tests                         | pytes                      | Y                 |
| Minimum coverage              | pytest --cov-fail-under=80 | Y                 |
| Audit vulnerabilities         | pip-audit                  | Y                 |
| Docker images vulnerabilities | trivy                      | Y                 |
| Exposed secrets               | gitleaks                   | Y                 |
## 8.2 Releases
- Semantic Versioning: MAJOR.MINOR.PATCH
- Tag GIT `v0.1.0` created automatically after merge in main

# 9. Useful commands
```

# ── Local ──────────────────────────────────────────────
cd python_service
pip install -r requirements.txt -r requirements-dev.txt

# Run tests
pytest tests/ -v --tb=short

# Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80

# Linting and formats
black app/ tests/
ruff check app/ tests/

# ── Docker ────────────────────────────────────────────────────────────
# Build
docker compose build --no-cache

# Service up
docker compose up -d

# healthcheck
docker compose ps     # all must be health or running

# ── manual check ────────────────────────────────────────────────
curl http://localhost:8000/health
curl -X POST http://localhost:8000/attachmentProcessingService -F "file=@test.pdf"
```

---
# 10. Behavioral rules

This section defines how the agent works - not what the system do

## 10.1 Before any action
- Confirm if SPEC.md ad plan.md were readen in the actual session;
- Check CHANGELOG.md to understand actual project state;

## 10.2 When ambiguity is found
- Do not solve it by yourself
- Raise a question asking cleary on how to proceed, I will decide

## 10.3 When creating a new file
- Check if the file fits the existing files structure (topic 3)
- Create the correspondent test before (TDD)
- Immediately include the docstring
- CHANGELOG.md updated after the task ends

## 10.4 When updating existing files
- Check if the tests are still successful

## 10.5 Tokens saving

The agent MUST prioritize project knowledge before thinking from scratch


| SOURCE           | WHEN USE IT                               |
| ---------------- | ----------------------------------------- |
| SPEC.md          | Always, before any session                |
| plan.md          | To understand the current task            |
| CHANGELOG.md     | To understand what was done               |
| docs/ADR         | Architectural decisions                   |
| Code docstrings  | Before asking what this function do       |
| requirements.txt | Before suggesting to add a new dependency |

## 10.6 What not to do without permission
- Change pinned docker versions
- Add new dependency on requirements.txt
- Delete tests files
- Change the directory structure
- Commit with credentials, even in placeholders

---
# 11. Actual project state

`Update this section after every reached milestone`


| MILESTONE                                   | STATUS      | REFERENCE                                          |
| ------------------------------------------- | ----------- | -------------------------------------------------- |
| M0 - Docker + python services orchestration | CONCLUDED   | ADR 001, CHANGELOG v0.1.0                          |
| M1 - Pipeline CI/CD                         | CONCLUDED   | ADR 003, CHANGELOG v0.2.0                          |

Actual version: `v0.2.0`
Last CHANGELOG: `[0.2.0] - 2026-04-23`
ADRs: `001-docker-python-services-orchestration`, `002-Multi format attachment processing strategy`, `003-github-actions-ci-cd-pipeline`