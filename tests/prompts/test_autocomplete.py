# -*- coding: utf-8 -*-

import pytest

from questionary.utils import is_prompt_toolkit_3
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


@pytest.mark.skipif(is_prompt_toolkit_3(), reason="autocomplete tests do not work with"
                                                  "prompt toolkit 3")
def test_use_tab_autocomplete():
    message = "Pick your poison"
    text = KeyInputs.TAB + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"
    kwargs = {
        "choices": ["python3", "python2", "python123"],
    }
    result, cli = feed_cli_with_input("autocomplete", message, text, **kwargs)
    assert result == "python2"


@pytest.mark.skipif(is_prompt_toolkit_3(), reason="autocomplete tests do not work with"
                                                  "prompt toolkit 3")
def test_use_key_tab_autocomplete():
    message = "Pick your poison"
    text = "p" + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"
    kwargs = {
        "choices": ["python3", "python2", "python123", "c++"],
    }
    result, cli = feed_cli_with_input("autocomplete", message, text, **kwargs)
    assert result == "python123"


@pytest.mark.skipif(is_prompt_toolkit_3(), reason="autocomplete tests do not work with"
                                                  "prompt toolkit 3")
def test_column_autocomplete():
    message = "Pick"
    kwargs = {"choices": ["a", "b", "c"]}
    text = KeyInputs.TAB + KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.ENTER + "\r"
    result, cli = feed_cli_with_input("autocomplete", message, text, **kwargs)
    assert result == "b"


@pytest.mark.skipif(is_prompt_toolkit_3(), reason="autocomplete tests do not work with"
                                                  "prompt toolkit 3")
def test_ignore_case_autocomplete():
    message = ("Pick your poison",)
    kwargs = {
        "choices": ["python3", "python2"],
    }
    text = "P" + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"
    result, cli = feed_cli_with_input(
        "autocomplete", message, text, **kwargs, ignore_case=False
    )
    assert result == "P"

    text = "p" + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input(
        "autocomplete", message, text, **kwargs, ignore_case=True
    )
    assert result == "python2"


@pytest.mark.skipif(is_prompt_toolkit_3(), reason="autocomplete tests do not work with"
                                                  "prompt toolkit 3")
def test_match_middle_autocomplete():
    message = ("Pick your poison",)
    kwargs = {
        "choices": ["python3", "python2"],
    }
    text = "t" + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"
    result, cli = feed_cli_with_input(
        "autocomplete", message, text, **kwargs, match_middle=False
    )
    assert result == "t"

    result, cli = feed_cli_with_input(
        "autocomplete", message, text, **kwargs, match_middle=True
    )
    assert result == "python2"
