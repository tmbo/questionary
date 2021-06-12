# -*- coding: utf-8 -*-
import pytest

from questionary import Separator, Choice
from tests.utils import feed_cli_with_input, KeyInputs, patched_prompt


def test_legacy_name():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("list", message, text, **kwargs)
    assert result == "foo"


def test_select_first_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_select_first_choice_with_token_title():
    message = "Foo message"
    kwargs = {
        "choices": [
            Choice(title=[("class:text", "foo")]),
            Choice(title=[("class:text", "bar")]),
            Choice(title=[("class:text", "bazz")]),
        ]
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_select_second_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bar"


def test_select_second_choice_using_j():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = "j" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bar"


def test_select_third_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_select_with_instruction():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"], "instruction": "sample instruction"}
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_cycle_to_first_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_cycle_backwards():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.UP + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_cycle_backwards_using_k():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = "k" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_separator_down():
    message = "Foo message"
    kwargs = {"choices": ["foo", Separator(), "bazz"]}
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_separator_up():
    message = "Foo message"
    kwargs = {"choices": ["foo", Separator(), "bazz", Separator("--END--")]}
    text = KeyInputs.UP + KeyInputs.UP + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_select_random_input():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"]}
    text = "some random input" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_select_ctr_c():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"]}
    text = KeyInputs.CONTROLC

    with pytest.raises(KeyboardInterrupt):
        feed_cli_with_input("select", message, text, **kwargs)


def test_select_empty_choices():
    message = "Foo message"
    kwargs = {"choices": []}
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("select", message, text, **kwargs)


def test_select_initial_choice():
    message = "Foo message"
    choice = Choice("bazz")
    kwargs = {"choices": ["foo", choice], "default": choice}
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_select_initial_choice_string():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"], "default": "bazz"}
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_select_initial_choice_duplicate():
    message = "Foo message"
    choice = Choice("foo")
    kwargs = {"choices": ["foo", choice, "bazz"], "default": choice}
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_select_initial_choice_not_selectable():
    message = "Foo message"
    separator = Separator()
    kwargs = {"choices": ["foo", "bazz", separator], "default": separator}
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("select", message, text, **kwargs)


def test_select_initial_choice_non_existant():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"], "default": "bar"}
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("select", message, text, **kwargs)


def test_no_invalid_parameters_are_forwarded():
    # the `validate_while_typing` parameter is an additional parameter that
    # gets forwarded to the `PromptSession`. this checks that the parameter
    # isn't forwarded to a method that does not expect it
    patched_prompt(
        [
            {
                "type": "select",
                "name": "theme",
                "message": "What do you want to do?",
                "choices": [
                    "Order a pizza",
                    "Make a reservation",
                ],
            }
        ],
        text=KeyInputs.ENTER + "\r",
        validate_while_typing=False,
    )


def test_select_arrow_keys():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"], "use_arrow_keys": True}
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_select_shortcuts():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"], "use_shortcuts": True}
    text = "2" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_select_no_arrow_keys():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", "bazz"],
        "use_arrow_keys": False,
        "use_shortcuts": True,
    }
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_select_no_shortcuts():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", "bazz"],
        "use_arrow_keys": True,
        "use_shortcuts": False,
    }
    text = "2" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_select_default_has_arrow_keys():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"]}
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"
