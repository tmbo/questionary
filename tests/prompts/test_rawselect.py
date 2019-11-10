# -*- coding: utf-8 -*-
import uuid

import pytest

from questionary import Separator
from tests.utils import feed_cli_with_input, KeyInputs


def test_legacy_name():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = "1" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("rawlist", message, text, **kwargs)
    assert result == "foo"


def test_select_first_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = "1" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("rawselect", message, text, **kwargs)
    assert result == "foo"


def test_select_second_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = "2" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("rawselect", message, text, **kwargs)
    assert result == "bar"


def test_select_third_choice():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bar", "bazz"]}
    text = "2" + "3" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("rawselect", message, text, **kwargs)
    assert result == "bazz"


def test_separator_shortcuts():
    message = "Foo message"
    kwargs = {"choices": ["foo", Separator(), "bazz"]}
    text = "2" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("rawselect", message, text, **kwargs)
    assert result == "bazz"


def test_duplicated_shortcuts():
    message = "Foo message"
    kwargs = {
        "choices": [
            {"name": "foo", "key": 1},
            Separator(),
            {"name": "bar", "key": 1},
            "bazz",
            Separator("--END--"),
        ]
    }
    text = "1" + KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("rawselect", message, text, **kwargs)


def test_invalid_shortcuts():
    message = "Foo message"
    kwargs = {
        "choices": [
            {"name": "foo", "key": "asd"},
            Separator(),
            {"name": "bar", "key": "1"},
            "bazz",
            Separator("--END--"),
        ]
    }
    text = "1" + KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("rawselect", message, text, **kwargs)


def test_to_many_choices():
    message = "Foo message"
    kwargs = {"choices": [uuid.uuid4().hex for _ in range(0, 37)]}
    text = "1" + KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input("rawselect", message, text, **kwargs)


def test_select_random_input():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"]}
    text = "2" + "some random input" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input("rawselect", message, text, **kwargs)
    assert result == "bazz"


def test_select_ctr_c():
    message = "Foo message"
    kwargs = {"choices": ["foo", "bazz"]}
    text = KeyInputs.CONTROLC

    with pytest.raises(KeyboardInterrupt):
        feed_cli_with_input("rawselect", message, text, **kwargs)
