import asyncio

from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from pytest import fail

from questionary import text
from tests.utils import KeyInputs


def test_ask_should_catch_keyboard_exception():
    inp = create_pipe_input()

    try:
        inp.send_text(KeyInputs.CONTROLC)
        question = text("Hello?", input=inp, output=DummyOutput())

        result = question.ask()
        assert result is None
    except KeyboardInterrupt:
        fail("Keyboard Interrupt should be caught by `ask()`")
    finally:
        inp.close()


def test_skipping_of_questions():
    inp = create_pipe_input()
    try:
        question = text("Hello?", input=inp, output=DummyOutput()).skip_if(
            condition=True, default=42
        )
        response = question.ask()
        assert response == 42
    finally:
        inp.close()


def test_skipping_of_skipping_of_questions():
    inp = create_pipe_input()
    try:
        inp.send_text("World" + KeyInputs.ENTER + "\r")

        question = text("Hello?", input=inp, output=DummyOutput()).skip_if(
            condition=False, default=42
        )

        response = question.ask()

        assert response == "World" and not response == 42
    finally:
        inp.close()


def test_async_ask_question():
    loop = asyncio.new_event_loop()

    inp = create_pipe_input()
    try:
        inp.send_text("World" + KeyInputs.ENTER + "\r")
        question = text("Hello?", input=inp, output=DummyOutput())
        response = loop.run_until_complete(question.ask_async())
        assert response == "World"
    finally:
        inp.close()
