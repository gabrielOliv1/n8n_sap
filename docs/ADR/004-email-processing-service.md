# ADR-004: Email Processing Service

**Date:** 2026-05-01  
**Status:** Accepted  
**Deciders:** Gabriel Oliveira  

---

## Context

The legacy `POST /attachmentProcessingService` endpoint accepted a single file via `multipart/form-data`. The actual n8n workflow produces a **JSON array** of emails — each potentially containing multiple base64-encoded attachments — making the old interface misaligned with real production payloads.

ADR-002 identified the impedance mismatch and recommended a pre-processing JSON strategy. M2 implements it.

---

## Decision

Create `POST /emailProcessingService` — a new endpoint that:

1. Accepts `application/json` with the exact array schema produced by n8n.
2. Applies a transformation pipeline to each email before returning results.
3. Keeps the old `/attachmentProcessingService` endpoint active (temporary deprecation period).

---

## Payload Contract

n8n actual output (source of truth for M2):

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
    "text": "sem docs\n\nEnviado com um e-mail seguro do provider email"
  }
]
```

---

## Transformation Pipeline

| Field | Raw Input | Transformation | Output |
|-------|-----------|---------------|--------|
| `requisitioner` | `'From: "name" <email@host.com>'` | Regex extract `<...>` content | `email@host.com` |
| `subject` | `'Subject: title'` | Strip `Subject:` prefix + trim | `title` |
| `text` | Body with footer | `text_cleaner.remove_email_footer()` + log | Clean body |
| `attachmentSummary` | base64 PDF data | Decode → pdfplumber → first 5k chars | `[{preview, fileName, fileType}]` |

---

## Attachment Parsing Scope (M2)

- **PDF only**: pdfplumber extracts text layer. Image-only PDFs return `preview: null`.
- **Non-PDF files** (ODT, DOCX, XLSX, CSV): `preview: null`. Full support deferred to M3.
- **Parse errors**: silently return `null` — a corrupt attachment must not abort the batch.
- **Size limit**: first 5 000 characters (≈ 1 250 tokens at 4 chars/token). Sufficient for LLM document classification.

---

## Footer Removal Strategy

Module `text_cleaner.py` maintains a `FOOTER_PATTERNS` list of compiled regexes:

| Pattern | Example match |
|---------|--------------|
| `Enviado (com\|de\|do\|desde\|pelo) .+` | Proton Mail, etc. (PT) |
| `Sent from .+` | iPhone, Android (EN) |
| `Enviado desde .+` | Spanish providers (ES) |
| `Envoyé depuis .+` | French providers (FR) |
| `Get Outlook for .+` | Outlook mobile |
| `--\s*\n.*` (DOTALL) | Standard `-- ` signature separator |

Every removal is logged at `INFO` level with `(email_id, removed_text)` for auditing and pattern discovery in production.

---

## n8n Workflow Change Required (Manual)

> [!IMPORTANT]
> After deploying M2, update the n8n HTTP Request node:
> - **URL**: `http://python:8000/attachmentProcessingService` → `http://python:8000/emailProcessingService`
> - **Content-Type**: `multipart/form-data` → `application/json`
> - **Body**: the JSON array built by the n8n merge node

---

## Consequences

### Positive
- Endpoint contract matches n8n's real output — no adapter layer needed.
- Transformation pipeline normalizes data before it reaches the LLM, reducing prompt engineering burden.
- Footer removal is extensible: add patterns to `FOOTER_PATTERNS` without touching business logic.
- Graceful degradation: corrupt/unsupported attachments produce `null` preview instead of HTTP 500.

### Negative
- PDF-only parsing in M2 means non-PDF attachment previews are deferred.
- Old endpoint retained temporarily — tech debt to be cleaned in M3.

---

## Alternatives Considered

| Alternative | Reason Rejected |
|-------------|----------------|
| Keep multipart/form-data | n8n multipart handling is unreliable for batched emails (ADR-002) |
| Parse all file types in M2 | Over-scope; PDF-only is sufficient for LLM classification prototype |
| Move transformation to n8n | Increases n8n complexity; Python service is better suited for regex/text processing |

---

## References

- ADR-002: Multi-format attachment processing strategy
- plan.md: M2 milestone specification
- CHANGELOG: v0.4.0
