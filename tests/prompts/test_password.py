# -*- coding: utf-8 -*-
from tests.utils import feed_cli_with_input


def test_password_entry():
    message = "What is your password"
    text = "my password\r"

    result, cli = feed_cli_with_input("password", message, text)
    assert result == "my password"
