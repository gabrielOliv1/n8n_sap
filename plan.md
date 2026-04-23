# Reestruturação do Projeto Python + Docker para Integração n8n

Reestruturar o serviço Python (FastAPI) para ser corretamente consumido pelo container n8n, com orquestração Docker adequada, hot reload, segurança e testes.

---

## Problemas Identificados no Estado Atual

| # | Problema | Impacto |
|---|----------|---------|
| 1 | **Dockerfile copia todo o projeto** (`COPY . .`) mas o volume do compose monta apenas `./python_scripts:/app` | O container fica com estrutura inconsistente — o código no container não reflete a estrutura montada |
| 2 | **CMD do Dockerfile vs command do compose divergem** — Dockerfile: `python_scripts.app.main:app`, compose: `python_scripts.main:app` | Apenas um dos dois paths funciona; o outro gera `ModuleNotFoundError` |
| 3 | **Volume monta `./python_scripts` em `/app`** mas uvicorn referencia `python_scripts.main` | Dentro de `/app` não existe subdiretório `python_scripts`, os módulos ficam diretamente em `/app/app/` |
| 4 | **Sem `requirements.txt`** — dependências instaladas inline no Dockerfile | Sem lock de versões, builds não-reproduzíveis, impossível fazer `pip install --upgrade` controlado |
| 5 | **Sem `__init__.py`** nos pacotes Python | Imports relativos podem falhar dependendo da resolução de módulos |
| 6 | **Endpoint `/attachmentProcessingService` não tipado** | Parâmetro `file` não usa `UploadFile` do FastAPI — não recebe multipart/form-data corretamente |
| 7 | **Sem rede Docker explícita** | Containers dependem da rede default — nomeação do host `python` funciona mas sem isolamento |
| 8 | **Sem healthcheck** | Não há como detectar se o serviço Python está pronto antes do n8n fazer requests |
| 9 | **Schema LLM é um arquivo `.py` com JSON puro** | Deveria ser um Pydantic model ou um `.json` separado |

---

## Alterações Propostas

### Componente 1 — Estrutura de Pastas do Python

Reestruturar o projeto Python para seguir convenções FastAPI com separação clara de responsabilidades:

```
python_service/                    ← renomear de python_scripts
├── app/
│   ├── __init__.py
│   ├── main.py                    ← FastAPI app factory
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── attachment.py      ← POST /attachmentProcessingService
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── enums/
│   │   │   ├── __init__.py
│   │   │   └── purchase_type.py   ← manter existente
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── llm_classification.py  ← converter para Pydantic
│   └── services/
│       ├── __init__.py
│       └── attachment_processor.py ← lógica de processamento de anexos
├── tests/
│   ├── __init__.py
│   ├── conftest.py                ← fixtures do pytest
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_attachment_processor.py
│   └── integration/
│       ├── __init__.py
│       └── test_attachment_endpoint.py
├── requirements.txt               ← dependências pinadas
├── requirements-dev.txt           ← dependências de desenvolvimento
└── Dockerfile                     ← Dockerfile movido para dentro do serviço
```

#### [NEW] [requirements.txt](file:///c:/Users/gabri/Downloads/projetos/python_service/requirements.txt)
```
fastapi==0.115.12
uvicorn[standard]==0.34.2
python-multipart==0.0.20
pdfplumber==0.11.6
python-docx==1.1.2
```

#### [NEW] [requirements-dev.txt](file:///c:/Users/gabri/Downloads/projetos/python_service/requirements-dev.txt)
```
pytest==8.3.5
httpx==0.28.1
pytest-asyncio==0.25.3
```

#### [MODIFY] [main.py](file:///c:/Users/gabri/Downloads/projetos/python_scripts/app/main.py)
Criar app factory com registro de rotas:
```python
from fastapi import FastAPI
from app.api.routes import attachment

def create_app() -> FastAPI:
    application = FastAPI(
        title="N8N Python Service",
        description="Serviço de processamento de anexos para integração n8n",
        version="0.1.0",
    )
    application.include_router(attachment.router)
    return application

app = create_app()
```

#### [NEW] [attachment.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/api/routes/attachment.py)
Endpoint corretamente tipado para receber `multipart/form-data`:
```python
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.attachment_processor import process_file

router = APIRouter()

@router.post("/attachmentProcessingService")
async def process_attachment(file: UploadFile = File(...)):
    content = await process_file(file)
    return content
```

#### [NEW] [attachment_processor.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/services/attachment_processor.py)
Lógica de processamento extraída para service layer:
```python
from fastapi import UploadFile, HTTPException
import pdfplumber
from docx import Document
from io import BytesIO

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".csv", ".txt"}
MAX_FILE_SIZE_MB = 10

async def process_file(file: UploadFile) -> dict:
    # Validação de extensão e tamanho
    # Leitura baseada no tipo do arquivo
    # Retorno do conteúdo extraído
    ...
```

#### [MODIFY] [llmClassificationOutput.py → llm_classification.py](file:///c:/Users/gabri/Downloads/projetos/python_scripts/app/domain/schemas/llmClassificationOutput.py)
Converter JSON puro para Pydantic model:
```python
from pydantic import BaseModel
from app.domain.enums.purchase_type import PurchaseType

class LLMClassificationOutput(BaseModel):
    purchase_type: PurchaseType
    item_category: str
    material: str
    quantity: int
    price: float
    uom: str
    supplier: str
    plant: str
    buying_model: str
    recommended_flow: str
```

---

### Componente 2 — Dockerfile (Python Service)

#### [NEW] [Dockerfile](file:///c:/Users/gabri/Downloads/projetos/python_service/Dockerfile)

```dockerfile
FROM python:3.13-slim AS base

# Prevenir criação de .pyc e buffering
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências primeiro (cache de layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY ./app ./app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### [DELETE] [Dockerfile](file:///c:/Users/gabri/Downloads/projetos/Dockerfile)
Remover o Dockerfile da raiz (será substituído pelo novo dentro de `python_service/`).

---

### Componente 3 — Docker Compose

#### [MODIFY] [docker-compose.yml](file:///c:/Users/gabri/Downloads/projetos/docker-compose.yml)

```yaml
services:
  n8n:
    image: n8nio/n8n:1.76.1
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    env_file:
      - .env
    environment:
      - N8N_HOST=0.0.0.0
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - GENERIC_TIMEZONE=America/Sao_Paulo
      - TZ=America/Sao_Paulo
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSION=true
    volumes:
      - ./n8n_data:/home/node/.n8n
    networks:
      - app-network
    depends_on:
      python:
        condition: service_healthy

  python:
    build:
      context: ./python_service
      dockerfile: Dockerfile
    container_name: python
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./python_service/app:/app/app    # Hot reload: monta apenas o código
    command: >
      uvicorn app.main:app
      --host 0.0.0.0
      --port 8000
      --reload
      --reload-dir /app/app
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 10s
      timeout: 5s
      start-period: 10s
      retries: 3
    networks:
      - app-network

  cloudflared:
    image: cloudflare/cloudflared:2025.10.0
    container_name: cloudflared
    command: tunnel --no-autoupdate --url http://n8n:5678
    restart: unless-stopped
    depends_on:
      - n8n
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Mudanças-chave:**
- Volume monta `./python_service/app` → `/app/app` (path exato do código)
- `uvicorn app.main:app` — module path correto dentro do container
- `--reload-dir /app/app` — hot reload observa apenas o diretório de código
- Rede explícita `app-network` para isolamento
- `depends_on` com `condition: service_healthy` — n8n só sobe quando Python está saudável
- Imagens com versões pinadas

---

### Componente 4 — Arquivo `.env`

#### [MODIFY] [.env](file:///c:/Users/gabri/Downloads/projetos/.env)
Extrair credenciais do compose:

```env
# n8n
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=<TROCAR_PARA_SENHA_SEGURA>
N8N_ENCRYPTION_KEY=<GERAR_CHAVE_ALEATÓRIA>
```

#### [MODIFY] [.gitignore](file:///c:/Users/gabri/Downloads/projetos/.gitignore)
Adicionar exclusões críticas:

```gitignore
.env
__pycache__/
*.pyc
n8n_data/
.pytest_cache/
*.egg-info/
```

---

### Componente 5 — Endpoint `/health`

#### [NEW] [health.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/api/routes/health.py)

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
```

Registrado no `main.py` junto com as rotas de attachment.

---

### Componente 6 — Testes

#### [NEW] [conftest.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/conftest.py)

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
```

#### [NEW] [test_attachment_endpoint.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/integration/test_attachment_endpoint.py)

Edge cases a cobrir:

| Teste | Cenário | Resultado Esperado |
|-------|---------|-------------------|
| `test_upload_pdf` | Upload de PDF válido | 200 + conteúdo extraído |
| `test_upload_docx` | Upload de DOCX válido | 200 + conteúdo extraído |
| `test_upload_no_file` | Request sem arquivo | 422 Validation Error |
| `test_upload_unsupported_extension` | Upload de `.exe` | 400 Bad Request |
| `test_upload_empty_file` | Arquivo com 0 bytes | 400 ou resposta vazia tratada |
| `test_upload_oversized_file` | Arquivo > MAX_FILE_SIZE_MB | 413 Payload Too Large |
| `test_upload_corrupted_pdf` | PDF com bytes inválidos | 400 + mensagem de erro clara |
| `test_health_check` | GET /health | 200 + `{"status": "healthy"}` |

#### [NEW] [test_attachment_processor.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/unit/test_attachment_processor.py)

Testes unitários para a lógica de extração isolada (sem HTTP).

---

## Open Questions

> [!IMPORTANT]
> **1. Versão do n8n:** Você usa alguma funcionalidade específica do n8n v2.x? Se sim, precisamos ajustar a versão pinada. Se não, `1.76.1` é uma versão estável segura.

> [!IMPORTANT]
> **2. Cloudflared:** O tunnel está configurado sem credenciais persistentes. Você usa Cloudflare Tunnel com token de autenticação (`TUNNEL_TOKEN`)? Se sim, precisamos adicionar ao `.env`.

> [!IMPORTANT]
> **3. Dados n8n existentes:** O diretório `n8n_data/` contém um banco SQLite com workflows existentes. A reestruturação **não** altera esse volume, mas confirme se há workflows que referenciam o hostname `python` na URL `http://python:8000/attachmentProcessingService` — esse path continuará funcionando.

---

## Plano de Verificação

### Testes Automatizados
```bash
# Dentro do container python (ou localmente com venv)
cd python_service
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -v --tb=short

# Verificar build do Docker
docker compose build --no-cache

# Subir os serviços e verificar saúde
docker compose up -d
docker compose ps     # todos devem estar "healthy" ou "running"
```

### Verificação Manual
1. `curl http://localhost:8000/health` → deve retornar `{"status": "healthy"}`
2. `curl -X POST http://localhost:8000/attachmentProcessingService -F "file=@test.pdf"` → deve retornar conteúdo extraído
3. No n8n (http://localhost:5678), testar o workflow existente que faz HTTP Request para `http://python:8000/attachmentProcessingService`
4. Editar um arquivo `.py` no host e verificar que o uvicorn recarrega automaticamente (hot reload)
