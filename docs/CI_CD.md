# CI/CD Pipeline Strategy

> Referenced from SPEC.md §8. This document details the CI/CD pipeline implementation.

---

## Overview

The project uses **GitHub Actions** with two workflows:

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI** | `.github/workflows/ci.yml` | `push` (any branch) + `pull_request` → `master` | Run all quality, test, and security checks |
| **Release** | `.github/workflows/release.yml` | `push` → `master` (when `CHANGELOG.md` changes) | Auto-create git tag + GitHub Release |

---

## CI Workflow — Checks on Every Commit

Three parallel jobs run on **every push to any branch** and on Pull Requests targeting `master`, ensuring every commit is production-ready:

### Job 1: Code Quality (~30s)

| Check | Tool | Command | Blocks Merge? |
|-------|------|---------|---------------|
| Formatting | `black` | `black --check app/ tests/` | ✅ Yes |
| Linting | `ruff` | `ruff check app/ tests/` | ✅ Yes |
| Type checking | `mypy` | `mypy app/` | ✅ Yes |

### Job 2: Tests (~60s)

| Check | Tool | Command | Blocks Merge? |
|-------|------|---------|---------------|
| Unit + Integration tests | `pytest` | `pytest tests/ -v --tb=short` | ✅ Yes |
| Minimum coverage (80%) | `pytest-cov` | `--cov=app --cov-fail-under=80` | ✅ Yes |

### Job 3: Security (~90s)

| Check | Tool | Command | Blocks Merge? |
|-------|------|---------|---------------|
| Python dependency audit | `pip-audit` | `pip-audit -r requirements.txt` | ✅ Yes |
| Docker image scan | `trivy` | Scans `CRITICAL` and `HIGH` severity | ✅ Yes |
| Exposed secrets | `gitleaks` | Full history scan | ✅ Yes |

---

## Release Workflow — Automatic Versioning

**Triggered by**: merge to `master` when `CHANGELOG.md` is modified.

**Steps**:
1. Extracts the latest version from `CHANGELOG.md` (regex: `## [X.Y.Z]`)
2. Checks if the git tag `vX.Y.Z` already exists
3. If new: creates an annotated git tag and pushes it
4. Creates a GitHub Release with notes extracted from the changelog

**Versioning**: Semantic Versioning (`MAJOR.MINOR.PATCH`) as defined in SPEC.md §8.2.

---

## Running Checks Locally

Before pushing, run the same checks locally from the `python_service/` directory:

```bash
cd python_service
pip install -r requirements.txt -r requirements-dev.txt

# Code quality
black --check app/ tests/
ruff check app/ tests/
mypy app/

# Tests with coverage
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing --cov-fail-under=80

# Security
pip-audit -r requirements.txt
```

For Docker image scanning, install [trivy](https://aquasecurity.github.io/trivy/) locally:
```bash
docker build -t n8n-sap-python:local ./python_service
trivy image n8n-sap-python:local --severity CRITICAL,HIGH
```

For secrets scanning, install [gitleaks](https://github.com/gitleaks/gitleaks):
```bash
gitleaks detect --source . -v
```

---

## Branch Protection Rules (GitHub)

To enforce the CI pipeline, configure branch protection on `master`:

### Steps to Configure

1. Go to **GitHub → Repository → Settings → Branches**
2. Click **Add branch protection rule**
3. Set **Branch name pattern**: `master`
4. Enable the following:
   - ✅ **Require a pull request before merging**
     - ✅ Require approvals: `1` (optional, recommended)
   - ✅ **Require status checks to pass before merging**
     - ✅ Require branches to be up to date before merging
     - Search and add these status checks:
       - `Code Quality (black + ruff + mypy)`
       - `Tests (pytest + coverage ≥80%)`
       - `Security (pip-audit + trivy + gitleaks)`
   - ✅ **Do not allow bypassing the above settings**
5. Click **Save changes**

> **Note**: The status check names will only appear after the CI workflow has run at least once. Push the workflow files first, create a test PR, then configure the protection rules.

---

## Troubleshooting

### CI job fails on `black --check`
Run `black app/ tests/` locally to auto-format, then commit the changes.

### CI job fails on `ruff check`
Run `ruff check app/ tests/ --fix` to auto-fix. Review the changes before committing.

### `mypy` reports type errors
Fix the type annotations. Use `# type: ignore` sparingly and only with a comment explaining why.

### `pip-audit` finds vulnerabilities
Update the affected package in `requirements.txt` to a patched version. Check CVEs before updating (SPEC.md §6.3).

### `trivy` finds Docker image vulnerabilities
Usually caused by base image packages. Check if a newer `python:3.13-slim` patch is available. If the vulnerability is in the OS layer and not exploitable, you can add it to a `.trivyignore` file with justification.

### `gitleaks` detects a secret
If it's a false positive, add it to a `.gitleaksignore` file. If it's a real secret, rotate it immediately and use `git filter-repo` to remove it from history.

### Release workflow doesn't create a tag
Verify that `CHANGELOG.md` contains a version in the format `## [X.Y.Z]` and that the tag doesn't already exist.
