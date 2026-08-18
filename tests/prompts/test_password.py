# -*- coding: utf-8 -*-
import io

import pytest
from prompt_toolkit.input.defaults import create_pipe_input

import questionary
from tests.utils import feed_cli_with_input
from tests.utils import prompt_toolkit_version


def _feed_password_and_capture(text, **kwargs):
    """Run a password prompt and return the (result, rendered_output) tuple.

    Unlike ``feed_cli_with_input`` this uses a ``PlainTextOutput`` so the text
    that would be shown on screen can be inspected (e.g. to check masking).
    """
    from prompt_toolkit.output.plain_text import PlainTextOutput

    output = PlainTextOutput(stdout=io.StringIO())
    with create_pipe_input() as inp:
        inp.send_text(text)
        question = questionary.password("password", input=inp, output=output, **kwargs)
        result = question.unsafe_ask()
    output.stdout.seek(0)
    return result, output.stdout.read()


def test_password_entry():
    message = "What is your password"
    text = "my password\r"

    result, cli = feed_cli_with_input("password", message, text)
    assert result == "my password"


def test_password_custom_echo_still_returns_value():
    message = "What is your password"
    text = "my password\r"

    result, cli = feed_cli_with_input("password", message, text, echo="")
    assert result == "my password"


needs_ptk3 = pytest.mark.skipif(
    prompt_toolkit_version < (3, 0, 0),
    reason="PlainTextOutput is only available in prompt_toolkit 3",
)


@needs_ptk3
def test_password_masks_with_asterisks_by_default():
    result, output = _feed_password_and_capture("secret\r")

    assert result == "secret"
    assert "secret" not in output
    assert "*" * len("secret") in output


@needs_ptk3
def test_password_empty_echo_hides_input():
    result, output = _feed_password_and_capture("secret\r", echo="")

    assert result == "secret"
    # Nothing about the secret should be echoed, not even its length.
    assert "secret" not in output
    assert "*" not in output


@needs_ptk3
def test_password_custom_echo_character():
    result, output = _feed_password_and_capture("secret\r", echo="X")

    assert result == "secret"
    assert "secret" not in output
    assert "X" * len("secret") in output
    assert "*" not in output
