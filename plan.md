# M2 — Email Processing Service

Implement the `emailProcessingService` endpoint to replace the current `attachmentProcessingService`. The new service receives a **JSON array** from n8n containing email metadata (sender, subject, body) and optional base64-encoded attachments, following the strategy defined in **ADR-002**.

## Background

The current `POST /attachmentProcessingService` receives a single file via `multipart/form-data` (`UploadFile`). ADR-002 identified that n8n's multipart handling is poor for batched emails with multiple attachments, and decided on a **pre-processing base64 JSON payload** strategy instead.

The real n8n flow now produces a JSON array like:

```json
[
  {
    "email": "email_1",
    "attachment": {
      "attachment_0": {
        "mimeType": "application/vnd.oasis.opendocument.text",
        "fileExtension": "odt",
        "data": "<base64>",
        "fileName": "file_name.odt",
        "fileSize": "30.4 kB"
      }
    },
    "requisitioner": "From: \"testing\" <testing@email>",
    "subject": "Subject: teste 23/04 com docs",
    "text": "email body text\n\nEnviado com um e-mail seguro do provider email"
  },
  {
    "email": "email_0",
    "requisitioner": "From: \"gabriel.ov\" <testing@email>",
    "subject": "Subject: teste 23/04 sem docs",
    "text": "sem dodcs\n\nEnviado com um e-mail seguro do provider email"
  }
]
```

---

## Decisions (User-confirmed)

### Q1 — Text extraction scope
**Option C**: Flow-testing focus. Decode base64, implement a simple parse function **only for PDF**, ignore errors (return nothing on failure). Limit parsing to the **first 5,000 characters** — enough to give the LLM a document preview.

### Q2 — n8n workflow update
Manual update by user. Documentation must clearly indicate **where** the n8n workflow URL needs to change (`http://python:8000/attachmentProcessingService` → `http://python:8000/emailProcessingService`).

### Q3 — Response schema
**Option A** — Structured array with transformations:

```json
[
  {
    "email": "email_1",
    "requisitioner": "testing@email.com",
    "subject": "teste 23/04 com docs",
    "text": "xom doce",
    "attachmentSummary": [
      {
        "preview": "First 5000 characters of parsed PDF...",
        "fileName": "file_name.pdf",
        "fileType": "pdf"
      }
    ]
  },
  {
    "email": "email_0",
    "requisitioner": "testing@email.com",
    "subject": "teste 23/04 sem docs",
    "text": "sem dodcs"
  }
]
```

**Transformations applied:**
| Field | Transformation |
|-------|---------------|
| `requisitioner` | Extract email address only (strip `From: "name"` wrapper) |
| `subject` | Strip `Subject:` prefix (standard across all emails) |
| `text` | Remove auto-generated email footers using flexible regex patterns |
| `attachmentSummary` | Array of previews. Each: `preview` (first 5k chars parsed), `fileName`, `fileType` |

**Footer removal pipeline**: Must include a logging function that logs `(email_identifier, removed_text)` for every footer strip — critical for testing and pattern validation.

### Q4 — ADR-002 payload discrepancy
n8n actual output is the source of truth. ADR-002 docs will be updated later.

---

## User Review Required

> [!IMPORTANT]
> **Paradigm shift**: The current `attachmentProcessingService` (multipart/form-data with `UploadFile`) will be **deprecated**. The new `emailProcessingService` endpoint accepts `application/json`. The old endpoint is kept temporarily.

> [!IMPORTANT]
> **n8n workflow URL change required**: After this milestone, update the n8n HTTP Request node from `http://python:8000/attachmentProcessingService` to `http://python:8000/emailProcessingService`. The request body must be the JSON array (not multipart/form-data).

---

## Proposed Changes

### Component 1 — Pydantic Schemas (Domain Layer)

#### [NEW] [email_payload.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/domain/schemas/email_payload.py)

Inbound payload validation — models the raw n8n JSON:

```python
class AttachmentData(BaseModel):
    """Single attachment from n8n payload."""
    mimeType: str
    fileExtension: str
    data: str              # base64 encoded content
    fileName: str
    fileSize: str

class EmailPayload(BaseModel):
    """Single email item from the n8n JSON array."""
    email: str             # email identifier (e.g. "email_1")
    requisitioner: str     # raw sender (e.g. 'From: "name" <email>')
    subject: str           # raw subject (e.g. "Subject: title")
    text: str              # raw email body (includes provider footers)
    attachment: dict[str, AttachmentData] | None = None
```

#### [NEW] [email_response.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/domain/schemas/email_response.py)

Outbound response — cleaned, transformed data ready for LLM consumption:

```python
class AttachmentSummary(BaseModel):
    """Preview of a single parsed attachment."""
    preview: str | None = None   # first 5k chars of extracted text (PDF only for now)
    fileName: str
    fileType: str                # e.g. "pdf", "odt", "docx"

class EmailResult(BaseModel):
    """Processed email with cleaned fields and attachment previews."""
    email: str                                        # email identifier
    requisitioner: str                                # cleaned email address only
    subject: str                                      # subject without "Subject:" prefix
    text: str                                         # body without provider footers
    attachmentSummary: list[AttachmentSummary] | None = None  # None if no attachments
```

Response is `list[EmailResult]` — an array, because one or more emails can be sent.

---

### Component 2 — Service Layer

#### [NEW] [email_processor.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/services/email_processor.py)

Core orchestration:

```python
async def process_email_batch(emails: list[EmailPayload]) -> list[EmailResult]:
    """Process a batch of emails from n8n payload.

    For each email:
    1. Clean requisitioner (extract email address)
    2. Clean subject (strip "Subject:" prefix)
    3. Clean text (remove provider footers with logging)
    4. Decode + parse attachments (PDF only, first 5k chars)
    """
```

Key internal functions:
- `_extract_email_address(raw_requisitioner: str) -> str` — regex to extract email from `From: "name" <email>` format
- `_clean_subject(raw_subject: str) -> str` — strip `Subject:` prefix and trim
- `_clean_email_body(email_id: str, raw_text: str) -> str` — remove provider footers with regex, **log removed text**
- `_log_removed_footer(email_id: str, removed_text: str) -> None` — logging function for stripped footers
- `_process_attachments(attachments: dict[str, AttachmentData]) -> list[AttachmentSummary]` — decode + parse each
- `_decode_base64(data: str) -> bytes` — base64 decode, returns empty bytes on error
- `_extract_pdf_preview(pdf_bytes: bytes, max_chars: int = 5000) -> str | None` — pdfplumber parse, first 5k chars, None on any error

#### [NEW] [text_cleaner.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/services/text_cleaner.py)

Dedicated module for the footer-removal pipeline:

```python
import re
import logging

logger = logging.getLogger(__name__)

# Flexible regex patterns for common email provider/device footers
FOOTER_PATTERNS: list[re.Pattern] = [
    re.compile(r"Enviado (com|de|do|desde|pelo) .+", re.IGNORECASE),       # Portuguese providers
    re.compile(r"Sent from .+", re.IGNORECASE),                             # English: "Sent from my iPhone"
    re.compile(r"Enviado desde .+", re.IGNORECASE),                         # Spanish providers
    re.compile(r"Envoyé depuis .+", re.IGNORECASE),                         # French providers
    re.compile(r"Get Outlook for .+", re.IGNORECASE),                       # Outlook mobile
    re.compile(r"--\s*\n.*", re.DOTALL),                                    # Standard email signature separator
    # Extensible: add patterns here as new providers are identified
]

def remove_email_footer(email_id: str, text: str) -> str:
    """Remove auto-generated email footers using regex patterns.

    Logs every removed fragment with the email identifier for testing/auditing.
    """

def _log_removed_footer(email_id: str, removed_text: str) -> None:
    """Log the removed footer text for debugging and pattern validation."""
    logger.info("Footer removed | email=%s | removed_text=%s", email_id, removed_text)
```

---

### Component 3 — API Route

#### [NEW] [email.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/api/routes/email.py)

```python
@router.post("/emailProcessingService")
async def process_emails(payload: list[EmailPayload]) -> list[EmailResult]:
    results = await process_email_batch(payload)
    return results
```

#### [MODIFY] [main.py](file:///c:/Users/gabri/Downloads/projetos/python_service/app/main.py)

Register the new email router:

```python
from app.api.routes import attachment, health, email

application.include_router(email.router)
```

---

### Component 4 — Tests (TDD — written before implementation)

#### [NEW] [test_email_payload_schema.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/unit/test_email_payload_schema.py)

| Test | Scenario | Expected |
|------|----------|----------|
| `test_email_payload_with_attachment_valid` | Full payload with 1 attachment | Model validates |
| `test_email_payload_without_attachment_valid` | Email without attachment key | attachment is None |
| `test_email_payload_missing_required_field` | Missing `subject` | ValidationError |
| `test_email_payload_multiple_attachments` | 2 attachments in dict | Model validates both |
| `test_attachment_data_valid` | All fields present | Model validates |
| `test_attachment_data_missing_data_field` | No `data` field | ValidationError |

#### [NEW] [test_email_response_schema.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/unit/test_email_response_schema.py)

| Test | Scenario | Expected |
|------|----------|----------|
| `test_email_result_with_attachment_summary` | Full result with previews | Model validates |
| `test_email_result_without_attachment_summary` | No attachments | attachmentSummary is None |
| `test_attachment_summary_with_preview` | Preview with 5k chars | Model validates |
| `test_attachment_summary_without_preview` | Non-PDF file, no preview | preview is None |

#### [NEW] [test_text_cleaner.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/unit/test_text_cleaner.py)

| Test | Scenario | Expected |
|------|----------|----------|
| `test_remove_portuguese_provider_footer` | `"text\n\nEnviado com um e-mail seguro do Proton Mail"` | `"text"`, footer logged |
| `test_remove_english_sent_from_footer` | `"text\n\nSent from my iPhone"` | `"text"`, footer logged |
| `test_remove_outlook_footer` | `"text\n\nGet Outlook for iOS"` | `"text"`, footer logged |
| `test_remove_signature_separator` | `"text\n\n-- \nJohn Doe\nCompany"` | `"text"`, separator logged |
| `test_no_footer_present` | `"plain text without footer"` | Text unchanged, no log |
| `test_footer_logging_content` | Any footer match | Logger called with `(email_id, removed_text)` |
| `test_multiple_footer_patterns` | Text with 2 patterns | Both removed, both logged |

#### [NEW] [test_email_processor.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/unit/test_email_processor.py)

| Test | Scenario | Expected |
|------|----------|----------|
| `test_extract_email_address_standard` | `'From: "name" <user@test.com>'` | `"user@test.com"` |
| `test_extract_email_address_no_name` | `'From: user@test.com'` | `"user@test.com"` |
| `test_clean_subject_strips_prefix` | `"Subject: test title"` | `"test title"` |
| `test_clean_subject_no_prefix` | `"test title"` | `"test title"` |
| `test_decode_base64_valid` | Valid base64 string | Returns decoded bytes |
| `test_decode_base64_invalid` | Corrupted base64 | Returns empty bytes (no error) |
| `test_extract_pdf_preview_valid` | Valid PDF bytes | Returns first ≤5k chars |
| `test_extract_pdf_preview_non_pdf` | DOCX bytes | Returns None (ignored) |
| `test_extract_pdf_preview_corrupted` | Invalid bytes | Returns None (no error) |
| `test_process_email_batch_mixed` | 1 with attachment + 1 without | Results for both |
| `test_process_email_batch_empty` | Empty list | Empty list returned |

#### [NEW] [test_email_endpoint.py](file:///c:/Users/gabri/Downloads/projetos/python_service/tests/integration/test_email_endpoint.py)

| Test | Scenario | Expected HTTP |
|------|----------|---------------|
| `test_post_email_valid_with_attachment` | Valid JSON with base64 PDF | 200 + attachmentSummary with preview |
| `test_post_email_valid_without_attachment` | Valid JSON, no attachment | 200 + attachmentSummary is None |
| `test_post_email_batch_multiple` | 2 emails in array | 200 + 2 results |
| `test_post_email_empty_payload` | `[]` | 200 + empty array |
| `test_post_email_invalid_json` | Malformed body | 422 |
| `test_post_email_missing_required_fields` | Missing `email` field | 422 |
| `test_post_email_subject_cleaned` | `"Subject: test"` | subject = `"test"` |
| `test_post_email_requisitioner_cleaned` | `'From: "name" <a@b.com>'` | requisitioner = `"a@b.com"` |
| `test_post_email_footer_removed` | Body with provider footer | text without footer |

---

### Component 5 — Documentation

#### [NEW] [004-email-processing-service.md](file:///c:/Users/gabri/Downloads/projetos/docs/ADR/004-email-processing-service.md)

ADR documenting:
- Decision to create `/emailProcessingService` replacing `/attachmentProcessingService`
- JSON array contract (based on real n8n output)
- Data transformation pipeline (requisitioner, subject, text cleaning, attachment preview)
- PDF-only parsing scope for M2
- Footer removal strategy with extensible regex patterns

#### [MODIFY] [plan.md](file:///c:/Users/gabri/Downloads/projetos/plan.md)

Replace the entire outdated M0 content with the M2 milestone task.

#### [MODIFY] [SPEC.md](file:///c:/Users/gabri/Downloads/projetos/SPEC.md)

- Add M2 row to milestone table (section 11)
- Update file structure (section 3) with new files: `email.py`, `email_payload.py`, `email_response.py`, `email_processor.py`, `text_cleaner.py`

> [!IMPORTANT]
> **n8n workflow change needed (manual)**: After deployment, update the n8n HTTP Request node URL from `http://python:8000/attachmentProcessingService` to `http://python:8000/emailProcessingService`. Change the request content type from `multipart/form-data` to `application/json`. The body is the email array built by the n8n merge node. Document this in ADR-004 and CHANGELOG.

#### [UPDATE] [CHANGELOG.md](file:///c:/Users/gabri/Downloads/projetos/CHANGELOG.md)

After implementation: add `[0.4.0]` entry.

#### [UPDATE LATER] [ADR-002](file:///c:/Users/gabri/Downloads/projetos/docs/ADR/002-Multi%20format%20attachment%20processing%20strategy.md)

Update section 7 (JSON Payload) to match actual n8n output. Deferred — done after M2 completion.

---

## Proposed File Structure (after changes)

```
python_service/
├── app/
│   ├── main.py                          ← register email router
│   ├── api/
│   │   └── routes/
│   │       ├── attachment.py            ← DEPRECATED, kept temporarily
│   │       ├── email.py                 ← NEW: POST /emailProcessingService
│   │       └── health.py
│   ├── domain/
│   │   ├── enums/
│   │   │   └── purchase_type.py
│   │   └── schemas/
│   │       ├── email_payload.py         ← NEW: inbound request schemas
│   │       ├── email_response.py        ← NEW: outbound response schemas
│   │       └── llm_classification.py
│   └── services/
│       ├── attachment_processor.py      ← DEPRECATED, kept temporarily
│       ├── email_processor.py           ← NEW: orchestration + base64 + PDF parse
│       └── text_cleaner.py              ← NEW: footer removal pipeline + logging
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_attachment_processor.py
│   │   ├── test_email_payload_schema.py ← NEW
│   │   ├── test_email_response_schema.py← NEW
│   │   ├── test_email_processor.py      ← NEW
│   │   ├── test_text_cleaner.py         ← NEW
│   │   └── test_schemas.py
│   ├── integration/
│   │   ├── test_attachment_endpoint.py
│   │   └── test_email_endpoint.py       ← NEW
│   └── regression/
│       └── .gitkeep
```

---

## Execution Order (TDD cycle)

Following SPEC.md section 4 SDLC:

1. **Phase 1 — Context** ✅ (done)
2. **Phase 2 — Tests first (RED)**
   - `test_email_payload_schema.py` → RED
   - `test_email_response_schema.py` → RED
   - `test_text_cleaner.py` → RED
   - `test_email_processor.py` → RED
   - `test_email_endpoint.py` → RED
3. **Phase 3 — Implementation (GREEN)**
   - `email_payload.py` + `email_response.py` → schema tests GREEN
   - `text_cleaner.py` → cleaner tests GREEN
   - `email_processor.py` → service tests GREEN
   - `email.py` route + `main.py` update → integration tests GREEN
4. **Phase 4 — Refactor**
   - Function length ≤30 lines, module length ≤200 lines
   - DRY review across services
5. **Phase 5 — Release**
   - ADR-004 created
   - plan.md updated to M2
   - CHANGELOG.md v0.4.0
   - SPEC.md milestone table + file structure updated

---

## Verification Plan

### Automated Tests
```bash
cd python_service
pytest tests/ -v --tb=short
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80
```

### Manual Verification
1. `docker compose up` — all services healthy
2. POST with n8n payload (with base64 PDF attachment) → 200 + preview in response
3. POST with email without attachment → 200 + attachmentSummary is None
4. Check logs for footer removal entries
5. Verify old endpoint still works: `curl -X POST http://localhost:8000/attachmentProcessingService -F "file=@test.pdf"` → 200
