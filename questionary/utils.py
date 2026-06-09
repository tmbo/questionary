import inspect
import shutil
import textwrap
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Set

from prompt_toolkit.application.current import get_app_or_none

from questionary.constants import DEFAULT_TERMINAL_WIDTH

ACTIVATED_ASYNC_MODE = False


def _current_terminal_width() -> int:
    """Return the terminal width as currently seen by the renderer.

    When called during a prompt-toolkit render pass, the running
    Application knows the live screen size (it tracks SIGWINCH).
    Querying it directly therefore returns a value that updates after a
    terminal resize, while shutil.get_terminal_size may return stale
    data if stdout has been replaced — which it is during a prompt
    session.

    Falls back to shutil.get_terminal_size outside of a prompt session
    (e.g. unit tests), and to DEFAULT_TERMINAL_WIDTH if neither source
    is usable.
    """
    app = get_app_or_none()
    if app is not None:
        columns = app.output.get_size().columns
        if columns > 0:
            return columns
    try:
        columns = shutil.get_terminal_size().columns
    except (OSError, ValueError):
        return DEFAULT_TERMINAL_WIDTH
    return columns if columns > 0 else DEFAULT_TERMINAL_WIDTH


def _wrap_message_to_terminal_width(message: Any, prefix_width: int = 0) -> Any:
    """Wrap message to the current terminal width.

    prompt-toolkit only line-wraps the input buffer window, not the
    prompt text rendered above it. When a message contains a newline,
    prompt-toolkit splits at the last newline and renders everything
    before it in a non-wrapping window — long lines then overflow the
    terminal width (see https://github.com/tmbo/questionary/issues/398).

    Pre-wrapping each newline-separated paragraph of the message to the
    terminal width sidesteps that: the rendered lines are already short
    enough that wrapping is unnecessary.

    Non-string messages (e.g. already-formatted text tuples) are
    returned unchanged so callers passing pre-styled prompts are not
    disturbed.

    Args:
        message: The user-provided message. Only plain str is wrapped;
            other types pass through unchanged.
        prefix_width: Number of cells reserved on the first line for any
            prefix (e.g. the question mark plus a separating space).

    Returns:
        message with additional newlines inserted so that no line
        exceeds the terminal width, or the original message unchanged
        if it was not a plain string.
    """
    if not isinstance(message, str) or not message:
        return message
    width = _current_terminal_width()
    # Pathologically narrow terminals: don't try to wrap, just hand the
    # message back and let the terminal do its worst.
    if width < 2:
        return message
    paragraphs = message.split("\n")
    wrapped: List[str] = []
    for i, paragraph in enumerate(paragraphs):
        if not paragraph:
            wrapped.append("")
            continue
        first = i == 0
        paragraph_width = max(width - prefix_width, 1) if first else max(width, 1)
        wrapped.append(
            textwrap.fill(
                paragraph,
                width=paragraph_width,
                break_long_words=False,
                break_on_hyphens=False,
                drop_whitespace=False,
                replace_whitespace=False,
            )
            or paragraph
        )
    return "\n".join(wrapped)


def is_prompt_toolkit_3() -> bool:
    from prompt_toolkit import __version__ as ptk_version

    return ptk_version.startswith("3.")


def default_values_of(func: Callable[..., Any]) -> List[str]:
    """Return all parameter names of ``func`` with a default value."""

    signature = inspect.signature(func)
    return [
        k
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
        or v.kind != inspect.Parameter.POSITIONAL_OR_KEYWORD
    ]


def arguments_of(func: Callable[..., Any]) -> List[str]:
    """Return the parameter names of the function ``func``."""

    return list(inspect.signature(func).parameters.keys())


def used_kwargs(kwargs: Dict[str, Any], func: Callable[..., Any]) -> Dict[str, Any]:
    """Returns only the kwargs which can be used by a function.

    Args:
        kwargs: All available kwargs.
        func: The function which should be called.

    Returns:
        Subset of kwargs which are accepted by ``func``.
    """

    possible_arguments = arguments_of(func)

    return {k: v for k, v in kwargs.items() if k in possible_arguments}


def required_arguments(func: Callable[..., Any]) -> List[str]:
    """Return all arguments of a function that do not have a default value."""
    defaults = default_values_of(func)
    args = arguments_of(func)

    if defaults:
        args = args[: -len(defaults)]
    return args  # all args without default values


def missing_arguments(func: Callable[..., Any], argdict: Dict[str, Any]) -> Set[str]:
    """Return all arguments that are missing to call func."""
    return set(required_arguments(func)) - set(argdict.keys())


async def activate_prompt_toolkit_async_mode() -> None:
    """Configure prompt toolkit to use the asyncio event loop.

    Needs to be async, so we use the right event loop in py 3.5"""
    global ACTIVATED_ASYNC_MODE

    if not is_prompt_toolkit_3():
        # Tell prompt_toolkit to use asyncio for the event loop.
        import prompt_toolkit as pt

        pt.eventloop.use_asyncio_event_loop()  # type: ignore[attr-defined]

    ACTIVATED_ASYNC_MODE = True
