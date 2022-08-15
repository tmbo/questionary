import asyncio
import platform

import pytest
from prompt_toolkit.output import DummyOutput
from pytest import fail

from questionary import text
from questionary.utils import is_prompt_toolkit_3
from tests.utils import KeyInputs
from tests.utils import execute_with_input_pipe


def test_ask_should_catch_keyboard_exception():
    def run(inp):
        inp.send_text(KeyInputs.CONTROLC)
        question = text("Hello?", input=inp, output=DummyOutput())
        try:
            result = question.ask()
            assert result is None
        except KeyboardInterrupt:
            fail("Keyboard Interrupt should be caught by `ask()`")

    execute_with_input_pipe(run)


def test_skipping_of_questions():
    def run(inp):
        question = text("Hello?", input=inp, output=DummyOutput()).skip_if(
            condition=True, default=42
        )
        response = question.ask()
        assert response == 42

    execute_with_input_pipe(run)


def test_skipping_of_questions_unsafe():
    def run(inp):
        question = text("Hello?", input=inp, output=DummyOutput()).skip_if(
            condition=True, default=42
        )
        response = question.unsafe_ask()
        assert response == 42

    execute_with_input_pipe(run)


def test_skipping_of_skipping_of_questions():
    def run(inp):
        inp.send_text("World" + KeyInputs.ENTER + "\r")
        question = text("Hello?", input=inp, output=DummyOutput()).skip_if(
            condition=False, default=42
        )
        response = question.ask()
        assert response == "World" and not response == 42

    execute_with_input_pipe(run)


def test_skipping_of_skipping_of_questions_unsafe():
    def run(inp):
        inp.send_text("World" + KeyInputs.ENTER + "\r")
        question = text("Hello?", input=inp, output=DummyOutput()).skip_if(
            condition=False, default=42
        )
        response = question.unsafe_ask()
        assert response == "World" and not response == 42

    execute_with_input_pipe(run)


@pytest.mark.skipif(
    not is_prompt_toolkit_3() and platform.system() == "Windows",
    reason="requires prompt_toolkit >= 3",
)
def test_async_ask_question():
    loop = asyncio.new_event_loop()

    def run(inp):
        inp.send_text("World" + KeyInputs.ENTER + "\r")
        question = text("Hello?", input=inp, output=DummyOutput())
        response = loop.run_until_complete(question.ask_async())
        assert response == "World"

    execute_with_input_pipe(run)


def test_multiline_text():
    def run(inp):
        inp.send_text(f"Hello{KeyInputs.ENTER}world{KeyInputs.ESCAPE}{KeyInputs.ENTER}")
        question = text("Hello?", input=inp, output=DummyOutput(), multiline=True)
        response = question.ask()
        assert response == "Hello\nworld"

    execute_with_input_pipe(run)
