from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Union

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import Style

from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.constants import NO
from questionary.constants import NO_OR_YES
from questionary.constants import YES
from questionary.constants import YES_OR_NO
from questionary.question import Question
from questionary.styles import merge_styles_default


def confirm(
    message: str,
    default: bool = True,
    qmark: str = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    auto_enter: bool = True,
    custom_key_bindings: Optional[Dict[Union[str, Keys], Callable]] = None,
    instruction: Optional[str] = None,
    **kwargs: Any,
) -> Question:
    """A yes or no question. The user can either confirm or deny.

    This question type can be used to prompt the user for a confirmation
    of a yes-or-no question. If the user just hits enter, the default
    value will be returned.

    Example:
        >>> import questionary
        >>> questionary.confirm("Are you amazed?").ask()
        ? Are you amazed? Yes
        True

    .. image:: ../images/confirm.gif

    This is just a really basic example, the prompt can be customised using the
    parameters.


    Args:
        message: Question text.

        default: Default value will be returned if the user just hits
                 enter.

        qmark: Question prefix displayed in front of the question.
               By default this is a ``?``.

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

        auto_enter: If set to `False`, the user needs to press the 'enter' key to
            accept their answer. If set to `True`, a valid input will be
            accepted without the need to press 'Enter'.

        custom_key_bindings: A dictionary specifying custom key bindings for the
                             prompt. The dictionary should have key-value pairs,
                             where the key represents the key combination or key
                             code, and the value is a callable that will be
                             executed when the key is pressed. The callable
                             should take an ``event`` object as its argument,
                             which will provide information about the key event.

                             Examples:

                             - Exit with a result of ``custom`` when the user
                               presses :kbd:`c`::

                                   {"c": lambda event: event.app.exit(result="custom")}

                             - Exit with a result of ``ctrl-q`` when the user
                               presses :kbd:`Ctrl` + :kbd:`q`::

                                   {Keys.ControlQ: lambda event: event.app.exit(result="ctrl-q")}

        instruction: A message describing how to proceed through the
                     confirmation prompt.
    Returns:
        :class:`Question`: Question instance, ready to be prompted (using `.ask()`).
    """
    merged_style = merge_styles_default([style])

    status = {"answer": None, "complete": False}

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", " {} ".format(message)))

        if instruction is not None:
            tokens.append(("class:instruction", "{} ".format(instruction)))
        elif not status["complete"]:
            _instruction = YES_OR_NO if default else NO_OR_YES
            tokens.append(("class:instruction", "{} ".format(_instruction)))

        if status["answer"] is not None:
            answer = YES if status["answer"] else NO
            tokens.append(("class:answer", answer))

        return to_formatted_text(tokens)

    def exit_with_result(event):
        status["complete"] = True
        event.app.exit(result=status["answer"])

    bindings = KeyBindings()
    if custom_key_bindings is not None:
        for key, func in custom_key_bindings.items():
            bindings.add(key, eager=True)(func)

    @bindings.add(Keys.ControlQ, eager=True)
    @bindings.add(Keys.ControlC, eager=True)
    def _(event):
        event.app.exit(exception=KeyboardInterrupt, style="class:aborting")

    @bindings.add("n")
    @bindings.add("N")
    def key_n(event):
        status["answer"] = False
        if auto_enter:
            exit_with_result(event)

    @bindings.add("y")
    @bindings.add("Y")
    def key_y(event):
        status["answer"] = True
        if auto_enter:
            exit_with_result(event)

    @bindings.add(Keys.ControlH)
    def key_backspace(event):
        status["answer"] = None

    @bindings.add(Keys.ControlM, eager=True)
    def set_answer(event):
        if status["answer"] is None:
            status["answer"] = default

        exit_with_result(event)

    @bindings.add(Keys.Any)
    def other(event):
        """Disallow inserting other text."""

    return Question(
        PromptSession(
            get_prompt_tokens, key_bindings=bindings, style=merged_style, **kwargs
        ).app
    )
