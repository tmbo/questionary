from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from pytest import fail

from questionary import text
from tests.utils import KeyInputs


def test_ask_should_catch_keyboard_exception():
    inp = create_pipe_input()

    try:
        inp.send_text(KeyInputs.CONTROLC)
        question = text("Hello?",
                        input=inp,
                        output=DummyOutput())

        result = question.ask()
        assert result is None
    except KeyboardInterrupt:
        fail("Keyboard Interrupt should be caught by `ask()`")
    finally:
        inp.close()


def test_skipping_of_questions():
    question = text("Hello?",
                    input=inp,
                    output=DummyOutput()).skip_if(condition=True, default=42)
    response = question.ask()
    assert response == 42


async def test_async_skipping_of_questions():
    question = text("Hello?",
                    input=inp,
                    output=DummyOutput()).skip_if(condition=True, default=42)
    response = await question.ask_async()
    assert response == 42


def test_skipping_of_skipping_of_questions():
    question = text("Hello?").skip_if(condition=False, default=42)
    response = "World"
    result = ask_with_patched_input(question, response)

    assert result == response and not result == 42
