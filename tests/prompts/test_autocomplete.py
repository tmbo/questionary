# -*- coding: utf-8 -*-

import pytest

from tests.utils import KeyInputs, feed_cli_with_input_async


# INFO: autocomplete tests need to be async as we need to sleep between
#       providing the CLI input and expecting the autocomplete to show
pytestmark = pytest.mark.asyncio


async def test_autocomplete():
    message = "Pick your poison "
    text = "python3\r"
    kwargs = {
        "choices": ["python3", "python2"],
    }
    result, cli = await feed_cli_with_input_async(
        "autocomplete", message, text, **kwargs
    )
    assert result == "python3"


async def test_no_choices_autocomplete():
    message = "Pick your poison "
    text = "python2\r"

    with pytest.raises(ValueError):
        await feed_cli_with_input_async("autocomplete", message, text, choices=[])


async def test_validate_autocomplete():
    message = "Pick your poison"
    text = "python123\r"

    kwargs = {
        "choices": ["python3", "python2", "python123"],
    }
    result, cli = await feed_cli_with_input_async(
        "autocomplete",
        message,
        text,
        validate=lambda x: "c++" not in x or "?",
        **kwargs,
    )
    assert result == "python123"


async def test_use_tab_autocomplete():
    message = "Pick your poison"
    texts = ["p", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]
    kwargs = {
        "choices": ["python3", "python2", "python123"],
    }
    result, cli = await feed_cli_with_input_async(
        "autocomplete", message, texts, **kwargs
    )
    assert result == "python2"


async def test_use_key_tab_autocomplete():
    message = "Pick your poison"
    texts = [
        "p",
        KeyInputs.TAB + KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r",
    ]
    kwargs = {
        "choices": ["python3", "python2", "python123", "c++"],
    }
    result, cli = await feed_cli_with_input_async(
        "autocomplete", message, texts, **kwargs
    )
    assert result == "python123"


async def test_ignore_case_autocomplete():
    message = ("Pick your poison",)
    kwargs = {
        "choices": ["python3", "python2"],
    }
    texts = ["P", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]
    result, cli = await feed_cli_with_input_async(
        "autocomplete", message, texts, **kwargs, ignore_case=False
    )
    assert result == "P"

    texts = ["p", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]

    result, cli = await feed_cli_with_input_async(
        "autocomplete", message, texts, **kwargs, ignore_case=True
    )
    assert result == "python2"


async def test_match_middle_autocomplete():
    message = ("Pick your poison",)
    kwargs = {
        "choices": ["python3", "python2"],
    }
    texts = ["t", KeyInputs.TAB + KeyInputs.TAB + KeyInputs.ENTER + "\r"]
    result, cli = await feed_cli_with_input_async(
        "autocomplete", message, texts, **kwargs, match_middle=False
    )
    assert result == "t"

    result, cli = await feed_cli_with_input_async(
        "autocomplete", message, texts, **kwargs, match_middle=True
    )
    assert result == "python2"
