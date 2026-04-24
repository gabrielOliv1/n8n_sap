# ADR 003 — GitHub Actions CI/CD Pipeline

## Status
Accepted

## Date
2026-04-23

## Context

The project reached milestone M0 (Docker + Python services orchestration) and needs automated quality gates before code reaches the `master` branch. SPEC.md §8 defines 8 mandatory checks that must pass on every PR. The pipeline must also automate semantic versioning and release creation (§8.2).

The team works with **feature branches + Pull Requests** to `master`.

## Decision

### CI Platform: GitHub Actions
- **Chosen**: GitHub Actions (native to GitHub, zero external dependencies)
- **Rejected**: Jenkins (heavy infrastructure), GitLab CI (different platform), CircleCI (external service, free tier limits)
- **Rationale**: Repository already hosted on GitHub. Actions provides free CI minutes for public repos and 2,000 min/month for private repos. No additional accounts or infrastructure needed.

### Workflow Architecture: 2 Workflows, 3 Parallel Jobs
- **CI workflow** (`ci.yml`): 3 jobs running in parallel on every PR
  - `quality` — black, ruff, mypy
  - `test` — pytest with coverage ≥80%
  - `security` — pip-audit, trivy, gitleaks
- **Release workflow** (`release.yml`): runs on merge to master when CHANGELOG.md changes
- **Rationale**: Parallel jobs reduce total CI time (~90s instead of ~180s sequential). Separating CI from Release keeps concerns isolated.

### Security Tools
- **trivy** (Aqua Security): Free, open source, scans Docker images for OS and library vulnerabilities. Filters `CRITICAL` and `HIGH` severity only to avoid noise.
- **gitleaks**: Industry standard for detecting hardcoded secrets in git history. Requires `GITLEAKS_LICENSE` secret for the GitHub Action (free for open source).
- **pip-audit** (PyPA): Scans Python dependencies against the Python Advisory Database. Official tool from the Python Packaging Authority.

### Release Strategy
- **Source of truth**: `CHANGELOG.md` — the version is extracted from the first `## [X.Y.Z]` heading
- **Tag format**: `vX.Y.Z` (annotated git tag)
- **Rationale**: CHANGELOG.md is already maintained as part of the SDLC (SPEC.md §4). Using it as the version source avoids duplication and ensures every release has documented changes.

## Consequences

### Positive
- Every PR is validated by 8 automated checks before merge
- No code with formatting issues, known vulnerabilities, or exposed secrets reaches master
- Releases are created automatically — no manual tagging needed
- Developers can run the same checks locally before pushing

### Negative
- CI adds ~90s to the PR feedback loop
- `gitleaks` GitHub Action requires a license secret (free for open source projects)
- `ignore_missing_imports = True` in mypy reduces type safety initially (necessary until third-party stubs are available)

### Risks
- **Trivy false positives**: Base image vulnerabilities may not be exploitable. Mitigation: `.trivyignore` with documented justification.
- **pip-audit lag**: Advisory database may not have the latest CVEs immediately. Mitigation: manual review on dependency updates.
