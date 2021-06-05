# -*- coding: utf-8 -*-
import pytest

from questionary import Separator, Choice
from tests.utils import feed_cli_with_input, KeyInputs


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


def test_select_third_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_select_third_choice_using_shortcuts_and_arrows():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", "bar", "bazz"],
        "use_shortcuts": True,
    }
    text = KeyInputs.TWO + KeyInputs.DOWN + KeyInputs.ENTER + "\r"
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



def test_disallow_shortcut_key():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", "bar", Choice("bazz", shortcut_key=False)],
        "use_shortcuts": True,
    }
    text = KeyInputs.THREE + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "foo"


def test_allow_shortcut_key_with_True():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", "bar", Choice("bazz", shortcut_key=True)],
        "use_shortcuts": True,
    }
    text = KeyInputs.THREE + "\r"

    result, cli = feed_cli_with_input("select", message, text, **kwargs)
    assert result == "bazz"


def test_fail_for_unreachable_choice():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", "bar", Choice("bazz", shortcut_key=False)],
        "use_shortcuts": True,
        "use_arrow_keys": False,
    }
    text = KeyInputs.THREE + "\r"

    with pytest.raises(RuntimeError):
        feed_cli_with_input("select", message, text, **kwargs)


def test_fail_on_no_method_to_move_selection():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", Choice("bar", disabled="bad"), "bazz"],
        "use_shortcuts": False,
        "use_arrow_keys": False,
    }
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("select", message, text, **kwargs)


def test_ij_and_shortcut_conflict_fails():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", Choice("bar", shortcut_key="i"), "bazz"],
        "use_shortcuts": True,
        "use_arrow_keys": True,
        "use_ij_keys": True,
    }
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("select", message, text, **kwargs)


def test_ij_and_shortcut_conflict_avoided_by_disabling_ij_keys():
    message = "Foo message"
    kwargs = {
        "choices": ["foo", Choice("bar", shortcut_key="i"), "bazz"],
        "use_shortcuts": True,
        "use_arrow_keys": True,
        "use_ij_keys": False,
    }
    text = KeyInputs.ENTER + "\r"

    feed_cli_with_input("select", message, text, **kwargs)
