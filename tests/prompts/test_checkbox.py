# -*- coding: utf-8 -*-
import pytest

from questionary import Choice
from questionary import Separator
from tests.utils import KeyInputs
from tests.utils import feed_cli_with_input


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


def test_select_with_instruction():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"], "instruction": "sample instruction"}
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


def test_select_disabled_choices_if_they_are_default():
    message = "Foo message"
    kwargs = {
        "choices": [
            Choice("foo", checked=True),
            Choice("bar", disabled="unavailable", checked=True),
            Choice("baz", disabled="unavailable"),
        ]
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo", "bar"]


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
        + "j"
        + KeyInputs.SPACE
        + KeyInputs.ENTER
        + "\r"
    )

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo", "bazz"]


def test_select_first_and_third_choice_using_emacs_keys():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = (
        KeyInputs.SPACE
        + KeyInputs.CONTROLN
        + KeyInputs.CONTROLN
        + KeyInputs.SPACE
        + KeyInputs.ENTER
        + "\r"
    )

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo", "bazz"]


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


def test_cycle_backwards_using_emacs_keys():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.CONTROLP + KeyInputs.SPACE + KeyInputs.ENTER + "\r"

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


def test_checkbox_initial_choice():
    message = "Foo message"
    choice = Choice("bazz")
    kwargs = {"choices": ["foo", choice], "initial_choice": choice}
    text = KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["bazz"]


def test_select_initial_choice_string():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"], "initial_choice": "bazz"}
    text = KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["bazz"]


def test_select_initial_choice_duplicate():
    message = "Foo message"
    choice = Choice("foo")
    kwargs = {"choices": ["foo", choice, "bazz"], "initial_choice": choice}
    text = KeyInputs.DOWN + KeyInputs.SPACE + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["bazz"]


def test_checkbox_initial_choice_not_selectable():
    message = "Foo message"
    separator = Separator()
    kwargs = {"choices": ["foo", "bazz", separator], "initial_choice": separator}
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("checkbox", message, text, **kwargs)


def test_checkbox_initial_choice_non_existant():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"], "initial_choice": "bar"}
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("checkbox", message, text, **kwargs)


def test_validate_default_message():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"], "validate": lambda a: len(a) != 0}
    text = KeyInputs.ENTER + "i" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo", "bar", "bazz"]


def test_validate_with_message():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", "bar", "bazz"],
        "validate": lambda a: True if len(a) > 0 else "Error Message",
    }
    text = KeyInputs.ENTER + "i" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == ["foo", "bar", "bazz"]


def test_validate_not_callable():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"], "validate": "invalid"}
    text = KeyInputs.ENTER + "i" + KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("checkbox", message, text, **kwargs)


def test_proper_type_returned():
    message = "Foo message"
    kwargs = {
        "choices": [
            Choice("one", value=1),
            Choice("two", value="foo"),
            Choice("three", value=[3, "bar"]),
        ]
    }
    text = (
        KeyInputs.SPACE
        + KeyInputs.DOWN
        + KeyInputs.SPACE
        + KeyInputs.DOWN
        + KeyInputs.SPACE
        + KeyInputs.DOWN
        + KeyInputs.ENTER
        + "\r"
    )

    result, cli = feed_cli_with_input("checkbox", message, text, **kwargs)
    assert result == [1, "foo", [3, "bar"]]


def test_fail_on_no_method_to_move_selection():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", Choice("bar", disabled="bad"), "bazz"],
        "use_shortcuts": False,
        "use_arrow_keys": False,
        "use_jk_keys": False,
        "use_emacs_keys": False,
    }
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("checkbox", message, text, **kwargs)
