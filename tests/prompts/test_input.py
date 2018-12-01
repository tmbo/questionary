# -*- coding: utf-8 -*-
from tests.utils import feed_cli_with_input


def test_input():
    message = 'What is your name'
    text = "bob\r"

    result, cli = feed_cli_with_input('input', message, text)
    assert result == 'bob'
