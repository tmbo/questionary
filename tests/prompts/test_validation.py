import asyncio
import inspect

import pytest
from prompt_toolkit.filters import Condition
from prompt_toolkit.output import DummyOutput

import questionary
from questionary.utils import is_prompt_toolkit_3
from tests.utils import execute_with_input_pipe
from tests.utils import feed_cli_with_input

PROMPTS = [
    questionary.text,
    questionary.password,
    questionary.path,
    questionary.autocomplete,
]


@pytest.mark.parametrize("prompt", PROMPTS)
def test_validate_while_typing_is_explicit_and_keyword_only(prompt):
    parameter = inspect.signature(prompt).parameters["validate_while_typing"]
    assert parameter.default is True
    assert parameter.kind == inspect.Parameter.KEYWORD_ONLY


@pytest.mark.parametrize("prompt", PROMPTS)
def test_validate_while_typing_accepts_filters(prompt):
    options = {"choices": ["valid"]} if prompt is questionary.autocomplete else {}

    def run(inp):
        question = prompt(
            "Value?",
            input=inp,
            output=DummyOutput(),
            validate_while_typing=Condition(lambda: False),
            **options,
        )
        assert not question.application.current_buffer.validate_while_typing()

    execute_with_input_pipe(run)


@pytest.mark.parametrize("prompt", PROMPTS)
@pytest.mark.parametrize("validate_while_typing", [True, False])
def test_validation_on_submit(prompt, validate_while_typing):
    calls = []

    def validate(value):
        calls.append(value)
        return value == "valid" or "Enter valid"

    options = {"choices": ["valid"]} if prompt is questionary.autocomplete else {}
    result, _ = feed_cli_with_input(
        prompt.__name__,
        "Value?",
        "invalid\r\x15valid\r",
        validate=validate,
        validate_while_typing=validate_while_typing,
        complete_while_typing=False,
        **options,
    )
    assert result == "valid"
    assert "invalid" in calls
    assert calls[-1] == "valid"


@pytest.mark.skipif(
    not is_prompt_toolkit_3(),
    reason="Live validation timing uses prompt_toolkit 3's asyncio loop",
)
@pytest.mark.parametrize("prompt", PROMPTS)
@pytest.mark.parametrize("validate_while_typing", [True, False])
def test_validation_timing_and_submit(prompt, validate_while_typing):
    async def run(inp):
        calls = []
        rendered = asyncio.Event()
        options = {"choices": ["valid"]} if prompt is questionary.autocomplete else {}

        def validate(value):
            calls.append(value)
            return value == "valid" or "Enter valid"

        question = prompt(
            "Value?",
            validate=validate,
            validate_while_typing=validate_while_typing,
            complete_while_typing=False,
            input=inp,
            output=DummyOutput(),
            **options,
        )
        app = question.application
        app.after_render += lambda _: rendered.set()

        async def wait_for_render(predicate):
            while not predicate():
                await asyncio.wait_for(rendered.wait(), timeout=5)
                rendered.clear()

        task = asyncio.create_task(question.unsafe_ask_async())
        try:
            await wait_for_render(lambda: app.is_running)
            inp.send_text("invalid")
            await wait_for_render(
                lambda: app.current_buffer.text == "invalid"
                and (not validate_while_typing or app.current_buffer.validation_error)
            )
            if validate_while_typing:
                assert "invalid" in calls
            else:
                assert calls == []
                inp.send_text("\r")
                await wait_for_render(lambda: app.current_buffer.validation_error)

            # Invalid input must be rejected even when live validation is off.
            assert not task.done()
            assert "invalid" in calls
            inp.send_text("\x15valid\r")
            assert await asyncio.wait_for(task, timeout=5) == "valid"
            assert calls[-1] == "valid"
        finally:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    execute_with_input_pipe(lambda inp: asyncio.run(run(inp)))
