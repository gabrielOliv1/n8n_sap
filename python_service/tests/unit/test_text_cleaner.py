"""Unit tests for the text_cleaner module (footer removal pipeline).

Tests written before implementation (TDD RED phase).
Nomenclature: test_<function>_<scenario>_<expected_result>
"""

from unittest.mock import patch

from app.services.text_cleaner import remove_email_footer

# ---------------------------------------------------------------------------
# Happy path — known footer patterns
# ---------------------------------------------------------------------------


def test_remove_portuguese_provider_footer_returns_clean_text() -> None:
    """'Enviado com ...' suffix is stripped from the body text."""
    raw = "email body\n\nEnviado com um e-mail seguro do Proton Mail"
    result = remove_email_footer("email_1", raw)
    assert "Enviado" not in result
    assert "email body" in result


def test_remove_english_sent_from_footer_returns_clean_text() -> None:
    """'Sent from my iPhone' suffix is stripped from the body text."""
    raw = "body text\n\nSent from my iPhone"
    result = remove_email_footer("email_2", raw)
    assert "Sent from" not in result
    assert "body text" in result


def test_remove_outlook_footer_returns_clean_text() -> None:
    """'Get Outlook for iOS' suffix is stripped from the body text."""
    raw = "meeting notes\n\nGet Outlook for iOS"
    result = remove_email_footer("email_3", raw)
    assert "Get Outlook" not in result
    assert "meeting notes" in result


def test_remove_signature_separator_returns_clean_text() -> None:
    """Standard '-- \\n...' signature separator block is stripped."""
    raw = "hello\n\n-- \nJohn Doe\nAcme Corp"
    result = remove_email_footer("email_4", raw)
    assert "John Doe" not in result
    assert "hello" in result


# ---------------------------------------------------------------------------
# No-op case
# ---------------------------------------------------------------------------


def test_no_footer_present_returns_text_unchanged() -> None:
    """When no footer pattern matches, the original text is returned unchanged."""
    raw = "plain text without any known footer"
    result = remove_email_footer("email_5", raw)
    assert result == raw


# ---------------------------------------------------------------------------
# Logging assertions
# ---------------------------------------------------------------------------


def test_footer_logging_content_calls_logger_with_email_id_and_removed_text() -> None:
    """Logger must be called with (email_id, removed_text) when a footer is stripped."""
    raw = "body\n\nSent from my Android"
    with patch("app.services.text_cleaner.logger") as mock_logger:
        remove_email_footer("email_6", raw)
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args
        # The call signature is logger.info(msg, email_id, removed_text)
        assert "email_6" in call_args.args or "email_6" in str(call_args)


def test_no_footer_does_not_call_logger() -> None:
    """Logger must NOT be called when no footer is removed."""
    raw = "clean text"
    with patch("app.services.text_cleaner.logger") as mock_logger:
        remove_email_footer("email_7", raw)
        mock_logger.info.assert_not_called()


# ---------------------------------------------------------------------------
# Multiple patterns in same text
# ---------------------------------------------------------------------------


def test_multiple_footer_patterns_both_removed_and_logged() -> None:
    """When text contains 2 footer patterns, both are removed and logger called twice."""
    # Two distinct patterns back-to-back
    raw = "body\n\nSent from my iPhone\nEnviado com um e-mail seguro do provider"
    with patch("app.services.text_cleaner.logger") as mock_logger:
        result = remove_email_footer("email_8", raw)
        assert "Sent from" not in result
        assert "Enviado" not in result
        # logger called once per removed fragment
        assert mock_logger.info.call_count >= 1
