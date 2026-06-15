# -*- coding: utf-8 -*-
import pytest

from tests.utils import KeyInputs
from tests.utils import feed_cli_with_input


def test_confirm_enter_default_yes():
    message = "Foo message"
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is True


def test_confirm_enter_default_no():
    message = "Foo message"
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, default=False)
    assert result is False


def test_confirm_yes():
    message = "Foo message"
    text = "y" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is True


def test_confirm_no():
    message = "Foo message"
    text = "n" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is False


def test_confirm_big_yes():
    message = "Foo message"
    text = "Y" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is True


def test_confirm_big_no():
    message = "Foo message"
    text = "N" + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is False


def test_confirm_random_input():
    message = "Foo message"
    text = "my stuff" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is True


def test_confirm_ctr_c():
    message = "Foo message"
    text = KeyInputs.CONTROLC

    with pytest.raises(KeyboardInterrupt):
        feed_cli_with_input("confirm", message, text)


def test_confirm_not_autoenter_yes():
    message = "Foo message"
    text = "n" + "y" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, auto_enter=False)
    assert result is True


def test_confirm_not_autoenter_no():
    message = "Foo message"
    text = "n" + "y" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, auto_enter=False)
    assert result is True


def test_confirm_not_autoenter_backspace():
    message = "Foo message"
    text = "n" + KeyInputs.BACK + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("confirm", message, text, auto_enter=False)
    assert result is True


def test_confirm_instruction():
    message = "Foo message"
    text = "Y" + "\r"

    result, cli = feed_cli_with_input(
        "confirm", message, text, instruction="Foo instruction"
    )
    assert result is True


def test_confirm_placeholder():
    message = "Foo message"
    text = "Y" + "\r"
    placeholder = "This is a placeholder"

    result, cli = feed_cli_with_input(
        "confirm", message, text, placeholder=placeholder
    )
    assert result is True


def test_confirm_placeholder_disappears_on_input():
    message = "Foo message"
    text = "n" + KeyInputs.ENTER + "\r"
    placeholder = "This should disappear"

    result, cli = feed_cli_with_input(
        "confirm", message, text, auto_enter=False, placeholder=placeholder
    )
    assert result is False
