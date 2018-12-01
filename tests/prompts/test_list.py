# -*- coding: utf-8 -*-
from tests.utils import feed_cli_with_input, KeyInputs


def test_select_first_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('list', message, text, **kwargs)
    assert result == 'foo'


def test_select_second_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('list', message, text, **kwargs)
    assert result == 'bar'


def test_select_third_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('list', message, text, **kwargs)
    assert result == 'bazz'


def test_cycle_to_first_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = (KeyInputs.DOWN + KeyInputs.DOWN +
            KeyInputs.DOWN + KeyInputs.ENTER + "\r")

    result, cli = feed_cli_with_input('list', message, text, **kwargs)
    assert result == 'foo'


def test_cycle_backwards():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.UP + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('list', message, text, **kwargs)
    assert result == 'bazz'
