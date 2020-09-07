# -*- coding: utf-8 -*-
import re

from prompt_toolkit.validation import Validator, ValidationError

from tests.utils import feed_cli_with_input


def test_legacy_name():
    message = "What is your name"
    text = "bob\r"

    result, cli = feed_cli_with_input("input", message, text)
    assert result == "bob"


def test_text():
    message = "What is your name"
    text = "bob\r"

    result, cli = feed_cli_with_input("text", message, text)
    assert result == "bob"


def test_text_validate():
    message = "What is your name"
    text = "Doe\r"

    result, cli = feed_cli_with_input(
        "text",
        message,
        text,
        validate=lambda val: val == "Doe" or "is your last name Doe?",
    )
    assert result == "Doe"


def test_text_validate_with_class():
    class SimpleValidator(Validator):
        def validate(self, document):
            ok = re.match("[01][01][01]", document.text)
            if not ok:
                raise ValidationError(
                    message="Binary FTW", cursor_position=len(document.text)
                )

    message = "What is your name"
    text = "001\r"

    result, cli = feed_cli_with_input("text", message, text, validate=SimpleValidator)
    assert result == "001"
