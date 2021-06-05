# -*- coding: utf-8 -*-
import pytest

from questionary import Separator, Choice
from tests.utils import feed_cli_with_input, KeyInputs


def test_submit_empty():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == []


def test_select_first_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo"]


def test_select_first_choice_with_token_title():
    message = "Foo message"
    kwargs = {
        "choices": [
            Choice(title=[("class:text", "foo")]),
            Choice(title=[("class:text", "bar")]),
            Choice(title=[("class:text", "bazz")]),
        ]
    }
    text = KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo"]


def test_select_and_deselct():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = (
        KeyInputs.SPACE
        + KeyInputs.DOWN
        + KeyInputs.SPACE
        + KeyInputs.SPACE
        + KeyInputs.ENTER
        + "\r"
    )

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo"]


def test_select_first_and_third_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    # DOWN and `j` should do the same
    text = (
        KeyInputs.SPACE
        + KeyInputs.DOWN
        + KeyInputs.SPACE
        + "j"
        + KeyInputs.ENTER
        + "\r"
    )

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo", "bar"]


def test_cycle_to_first_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = (
        KeyInputs.DOWN
        + KeyInputs.DOWN
        + KeyInputs.DOWN
        + KeyInputs.SPACE
        + KeyInputs.ENTER
        + "\r"
    )

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo"]


def test_cycle_backwards():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.UP + KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["bazz"]


def test_separator_down():
    message = "Foo message"
    kwargs = {"choices": ["foo", Separator(), "bazz"]}
    text = KeyInputs.DOWN + KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["bazz"]


def test_separator_up():
    message = "Foo message"
    kwargs = {"choices": ["foo", Separator(), "bazz", Separator("--END--")]}
    # UP and `k` should do the same
    text = KeyInputs.UP + "k" + KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo"]


def test_select_all():
    message = "Foo message"
    kwargs = {
        "choices": [
            {"name": "foo", "checked": True},
            Separator(),
            {"name": "bar", "disabled": "nope"},
            "bazz",
            Separator("--END--"),
        ]
    }
    text = KeyInputs.UP + "a" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo", "bazz"]


def test_select_all_deselect():
    message = "Foo message"
    kwargs = {
        "choices": [
            {"name": "foo", "checked": True},
            Separator(),
            {"name": "bar", "disabled": "nope"},
            "bazz",
            Separator("--END--"),
        ]
    }
    text = KeyInputs.UP + "a" + "a" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == []


def test_select_invert():
    message = "Foo message"
    kwargs = {
        "choices": [
            {"name": "foo", "checked": True},
            Separator(),
            {"name": "bar", "disabled": "nope"},
            "bazz",
            Separator("--END--"),
        ]
    }
    text = KeyInputs.UP + "i" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["bazz"]


def test_list_random_input():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"]}
    text = "sdf" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == []


def test_list_ctr_c():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"]}
    text = KeyInputs.CONTROLC

    with pytest.raises(KeyboardInterrupt):
        feed_cli_with_input("checkbox", message, text, **kwargs)
