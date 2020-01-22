# -*- coding: utf-8 -*-
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput

from questionary import prompt
from questionary.prompts import prompt_by_name


class KeyInputs(object):
    DOWN = "\x1b[B"
    UP = "\x1b[A"
    LEFT = "\x1b[D"
    RIGHT = "\x1b[C"
    ENTER = "\x0a"
    ESCAPE = "\x1b"
    CONTROLC = "\x03"
    BACK = "\x7f"
    SPACE = " "
    TAB = "\x09"


def feed_cli_with_input(_type, message, text, **kwargs):
    """
    Create a Prompt, feed it with the given user input and return the CLI
    object.
    This returns a (result, Application) tuple.
    """

    inp = create_pipe_input()

    try:
        # noinspection PyUnresolvedReferences
        inp.send_text(text)
        prompter = prompt_by_name(_type)
        application = prompter(message, input=inp, output=DummyOutput(), **kwargs)

        result = application.unsafe_ask()
        return result, application

    finally:
        inp.close()


def patched_prompt(questions, text, **kwargs):
    """Create a prompt where the input and output are predefined."""

    inp = create_pipe_input()

    try:
        inp.send_text(text)
        result = prompt(questions, input=inp, output=DummyOutput(), **kwargs)
        return result

    finally:
        inp.close()
