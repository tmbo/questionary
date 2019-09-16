# -*- coding: utf-8 -*-
import pytest

from questionary import Separator, Choice
from tests.utils import feed_cli_with_input, KeyInputs


def test_legacy_name():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('list', message, text, **kwargs)
    assert result == 'foo'


def test_select_first_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'foo'


def test_select_first_choice_with_token_title():
    message = 'Foo message'
    kwargs = {
        'choices': [
            Choice(title=[('class:text', 'foo')]),
            Choice(title=[('class:text', 'bar')]),
            Choice(title=[('class:text', 'bazz')])
        ]
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'foo'


def test_select_second_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'bar'


def test_select_third_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.DOWN + KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'bazz'

def test_select_third_choice_using_shortcuts_and_arrows():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz'],
        'use_shortcuts': True,
    }
    text = KeyInputs.TWO + KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'bazz'


def test_cycle_to_first_choice():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = (KeyInputs.DOWN + KeyInputs.DOWN +
            KeyInputs.DOWN + KeyInputs.ENTER + "\r")

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'foo'


def test_cycle_backwards():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz']
    }
    text = KeyInputs.UP + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'bazz'


def test_separator_down():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', Separator(), 'bazz']
    }
    text = KeyInputs.DOWN + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'bazz'


def test_separator_up():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', Separator(), 'bazz', Separator("--END--")]
    }
    text = KeyInputs.UP + KeyInputs.UP + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'foo'


def test_select_random_input():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bazz']
    }
    text = "some random input" + KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'foo'


def test_select_ctr_c():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bazz']
    }
    text = KeyInputs.CONTROLC

    with pytest.raises(KeyboardInterrupt):
        feed_cli_with_input('select', message, text, **kwargs)


def test_select_empty_choices():
    message = 'Foo message'
    kwargs = {
        'choices': []
    }
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(ValueError):
        feed_cli_with_input('select', message, text, **kwargs)

def test_start_at_second_choice_with_int():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', 'bazz'],
        'start': 1
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'bar'


def test_start_at_third_choice_with_title():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', Choice('bazz')],
        'start': 'bazz'
    }
    text = KeyInputs.ENTER + "\r"

    result, cli = feed_cli_with_input('select', message, text, **kwargs)
    assert result == 'bazz'


def test_fails_on_bad_title_start():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', Choice('bazz')],
        'start': 'bad'
    }
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(KeyError):
        feed_cli_with_input('select', message, text, **kwargs)

def test_fails_on_bad_index_start():
    message = 'Foo message'
    kwargs = {
        'choices': ['foo', 'bar', Choice('bazz')],
        'start': 100
    }
    text = KeyInputs.ENTER + "\r"

    with pytest.raises(IndexError):
        feed_cli_with_input('select', message, text, **kwargs)