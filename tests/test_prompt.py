import asyncio
from unittest.mock import patch

import pytest

from questionary.prompt import PromptParameterException
from questionary.prompt import prompt
from questionary.prompt import prompt_async
from tests.utils import patched_prompt


def test_missing_message():
    with pytest.raises(PromptParameterException):
        prompt([{"type": "confirm", "name": "continue", "default": True}])


def test_missing_type():
    with pytest.raises(PromptParameterException):
        prompt(
            [
                {
                    "message": "Do you want to continue?",
                    "name": "continue",
                    "default": True,
                }
            ]
        )


def test_missing_name():
    with pytest.raises(PromptParameterException):
        prompt(
            [
                {
                    "type": "confirm",
                    "message": "Do you want to continue?",
                    "default": True,
                }
            ]
        )


def test_invalid_question_type():
    with pytest.raises(ValueError):
        prompt(
            [
                {
                    "type": "mytype",
                    "message": "Do you want to continue?",
                    "name": "continue",
                    "default": True,
                }
            ]
        )


def test_missing_print_message():
    """Test 'print' raises exception if missing 'message'"""
    with pytest.raises(PromptParameterException):
        prompt(
            [
                {
                    "name": "test",
                    "type": "print",
                }
            ]
        )


def test_print_no_name():
    """'print' type doesn't require a name so it
    should not throw PromptParameterException"""
    questions = [{"type": "print", "message": "Hello World"}]
    result = patched_prompt(questions, "")
    assert result == {}


def test_print_with_name():
    """'print' type should return {name: None} when name is provided"""
    questions = [{"name": "hello", "type": "print", "message": "Hello World"}]
    result = patched_prompt(questions, "")
    assert result == {"hello": None}


@patch("builtins.print")
@patch("questionary.prompt.unsafe_prompt", side_effect=KeyboardInterrupt)
def test_no_keyboard_interrupt_message_in_prompt(
    mock_unsafe_prompt, mock_print
) -> None:
    """
    Test no message printed when `kbi_msg` is None in `prompt()`.

    Args:
        mock_unsafe_prompt: A mock of the internal `unsafe_prompt()` call.
            raises a KeyboardInterrupt.

        mock_print: A mock of Python's builtin `print()` function.
    """
    # Act
    result = prompt(questions={}, kbi_msg=None)

    # Verify internal functions were properly called
    mock_unsafe_prompt.assert_called_once()  # Raises KeyboardInterrupt
    mock_print.assert_not_called()

    # Verify result
    assert result == {}


@patch("builtins.print")
@patch("questionary.prompt.unsafe_prompt_async", side_effect=KeyboardInterrupt)
def test_no_keyboard_interrupt_message_in_prompt_async(
    mock_unsafe_prompt_async, mock_print
) -> None:
    """
    Test no message printed when `kbi_msg` is None in `prompt_async()`.

    Args:
        mock_unsafe_prompt_async: A mock of the internal `unsafe_prompt_async()` call.
            raises a KeyboardInterrupt.

        mock_print: A mock of Python's builtin `print()` function.
    """
    # Act
    result = asyncio.run(prompt_async(questions={}, kbi_msg=None))

    # Verify internal functions were properly called
    mock_unsafe_prompt_async.assert_called_once()  # Raises KeyboardInterrupt
    mock_print.assert_not_called()

    # Verify result
    assert result == {}
