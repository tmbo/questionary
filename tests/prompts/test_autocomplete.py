# -*- coding: utf-8 -*-

import pytest

from tests.utils import KeyInputs, feed_cli_with_input


def test_autocomplete():
    message = "Pick your poison "
    text = "python3\r"
    kwargs = {
        "choices": ["python3", "python2"],
    }
    result, cli = feed_cli_with_input("autocomplete", message, text, **kwargs)
    assert result == "python3"


def test_no_choices_autocomplete():
    message = "Pick your poison "
    text = "python2\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("autocomplete", message, text, choices=[])


def test_validate_autocomplete():
    message = "Pick your poison"
    text = "python123\r"

    kwargs = {
        "choices": ["python3", "python2", "python123"],
    }
    result, cli = feed_cli_with_input(
        "autocomplete",
        message,
        text,
        validate=lambda x: "c++" not in x or "?",
        **kwargs,
    )
    assert result == "python123"


def test_use_tab_autocomplete():
    message = "Pick your poison"
    texts = ["p", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]
    kwargs = {
        "choices": ["python3", "python2", "python123"],
    }
    result, cli = feed_cli_with_input("autocomplete", message, texts, **kwargs)
    assert result == "python2"


def test_use_key_tab_autocomplete():
    message = "Pick your poison"
    texts = [
        "p",
        KeyInputs.TAB + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r",
    ]
    kwargs = {
        "choices": ["python3", "python2", "python123", "c++"],
    }
    result, cli = feed_cli_with_input("autocomplete", message, texts, **kwargs)
    assert result == "python123"


def test_ignore_case_autocomplete():
    message = ("Pick your poison",)
    kwargs = {
        "choices": ["python3", "python2"],
    }
    texts = ["P", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]
    result, cli = feed_cli_with_input(
        "autocomplete", message, texts, **kwargs, ignore_case=False
    )
    assert result == "P"

    texts = ["p", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]

    result, cli = feed_cli_with_input(
        "autocomplete", message, texts, **kwargs, ignore_case=True
    )
    assert result == "python2"


def test_match_middle_autocomplete():
    message = ("Pick your poison",)
    kwargs = {
        "choices": ["python3", "python2"],
    }
    texts = ["t", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]
    result, cli = feed_cli_with_input(
        "autocomplete", message, texts, **kwargs, match_middle=False
    )
    assert result == "t"

    result, cli = feed_cli_with_input(
        "autocomplete", message, texts, **kwargs, match_middle=True
    )
    assert result == "python2"
