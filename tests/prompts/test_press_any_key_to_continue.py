# -*- coding: utf-8 -*-

from tests.utils import feed_cli_with_input


def test_press_any_key_to_continue_default_message():
    message = None
    text = "c"
    result, cli = feed_cli_with_input("press_any_key_to_continue", message, text)

    assert result is None
