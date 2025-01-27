# -*- coding: utf-8 -*-
import pytest

from tests.utils import KeyInputs
from tests.utils import feed_cli_with_input


def test_confirm_yes():
    """Test standard confirmation with 'y'."""
    message = "Foo message"
    text = "y" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is True


def test_confirm_no():
    """Test standard confirmation with 'n'."""
    message = "Foo message"
    text = "n" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is False


def test_confirm_big_yes():
    """Test standard confirmation with 'Y'."""
    message = "Foo message"
    text = "Y" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is True


def test_confirm_big_no():
    """Test standard confirmation with 'N'."""
    message = "Foo message"
    text = "N" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is False


def test_confirm_ctr_c():
    """Test handling of Ctrl+C interruption."""
    message = "Foo message"
    text = KeyInputs.CONTROLC

    with pytest.raises(KeyboardInterrupt):
        feed_cli_with_input("confirm", message, text)


def test_confirm_not_autoenter_yes():
    """Test confirm prompt without auto-enter when user types 'y'."""
    message = "Foo message"
    text = "n" + "y" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, auto_enter=False)
    assert result is True


def test_confirm_not_autoenter_no():
    """Test confirm prompt without auto-enter when user types 'n'."""
    message = "Foo message"
    text = "n" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, auto_enter=False)
    assert result is False


def test_confirm_not_autoenter_backspace():
    """Test confirm prompt where user backspaces to empty input and retypes."""
    message = "Foo message"
    text = "n" + KeyInputs.BACK + "y" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, auto_enter=False)
    assert result is True


def test_confirm_instruction():
    """Test confirm prompt with a custom instruction."""
    message = "Foo message"
    text = "Y" + "\r"

    result, cli = feed_cli_with_input(
        "confirm", message, text, instruction="Foo instruction"
    )
    assert result is True


def test_confirm_mandatory_yes():
    """Test mandatory confirm prompt when user explicitly types 'yes'."""
    message = "Foo message"
    text = "y" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, mandatory=True)
    assert result is True


def test_confirm_mandatory_no():
    """Test mandatory confirm prompt when user explicitly types 'no'."""
    message = "Foo message"
    text = "n" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, mandatory=True)
    assert result is False


def test_confirm_mandatory_reject_empty():
    """Test mandatory confirm prompt rejects empty input."""
    message = "Foo message"
    text = KeyInputs.ENTER + "y" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, mandatory=True)
    assert result is True


def test_confirm_mandatory_reject_invalid_input():
    """Test mandatory confirm prompt rejects invalid input."""
    message = "Foo message"
    text = "x" + KeyInputs.ENTER + "y" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, mandatory=True)
    assert result is True
