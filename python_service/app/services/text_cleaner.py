"""Footer removal pipeline for email body text.

Provides an extensible set of regex patterns to strip auto-generated footers
appended by email clients, mobile apps, and service providers. Every removed
fragment is logged for auditing and pattern validation.
"""

import logging
import re

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Extensible footer pattern registry
# Patterns are matched against the full email text (IGNORECASE where relevant).
# Add new patterns here as providers are identified in production logs.
# ---------------------------------------------------------------------------
FOOTER_PATTERNS: list[re.Pattern[str]] = [
    # Portuguese providers (Proton Mail, etc.)
    re.compile(r"Enviado (com|de|do|desde|pelo) .+", re.IGNORECASE),
    # English mobile footers: "Sent from my iPhone / Android / Galaxy"
    re.compile(r"Sent from .+", re.IGNORECASE),
    # Spanish providers
    re.compile(r"Enviado desde .+", re.IGNORECASE),
    # French providers
    re.compile(r"Envoyé depuis .+", re.IGNORECASE),
    # Outlook mobile
    re.compile(r"Get Outlook for .+", re.IGNORECASE),
    # Standard email signature separator: "-- \n<signature block>"
    re.compile(r"--\s*\n.*", re.DOTALL),
]


def remove_email_footer(email_id: str, text: str) -> str:
    """Remove auto-generated email footers from the body text.

    Iterates over FOOTER_PATTERNS and removes the first (leftmost) match of
    each pattern. Each removed fragment is logged via _log_removed_footer so
    that the removal pipeline can be audited and new patterns identified.

    Args:
        email_id: Internal n8n identifier for the email (e.g. 'email_1').
            Used exclusively for log correlation.
        text: Raw email body text that may contain provider footers.

    Returns:
        Cleaned body text with all matched footer patterns stripped and
        trailing whitespace removed.
    """
    cleaned = text
    for pattern in FOOTER_PATTERNS:
        match = pattern.search(cleaned)
        if match:
            removed_fragment = match.group(0)
            _log_removed_footer(email_id, removed_fragment)
            cleaned = cleaned[: match.start()]
    return cleaned.rstrip()


def _log_removed_footer(email_id: str, removed_text: str) -> None:
    """Log a removed footer fragment for debugging and pattern validation.

    Args:
        email_id: Internal n8n identifier for the email being processed.
        removed_text: The exact text fragment that was stripped from the body.
    """
    logger.info("Footer removed | email=%s | removed_text=%s", email_id, removed_text)
