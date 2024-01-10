from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from prompt_toolkit.document import Document
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.styles import Style

from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.constants import INSTRUCTION_MULTILINE
from questionary.prompts.common import build_validator
from questionary.question import Question
from questionary.styles import merge_styles_default


def text(
    message: str,
    default: str = "",
    validate: Any = None,
    qmark: str = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    multiline: bool = False,
    instruction: Optional[str] = None,
    lexer: Optional[Lexer] = None,
    custom_key_bindings: Optional[Dict[Union[str, Keys], Callable]] = None,
    **kwargs: Any,
) -> Question:
    """Prompt the user to enter a free text message.

    This question type can be used to prompt the user for some text input.

    Example:
        >>> import questionary
        >>> questionary.text("What's your first name?").ask()
        ? What's your first name? Tom
        'Tom'

    .. image:: ../images/text.gif

    This is just a really basic example, the prompt can be customised using the
    parameters.

    Args:
        message: Question text.

        default: Default value will be returned if the user just hits
                 enter.

        validate: Require the entered value to pass a validation. The
                  value can not be submitted until the validator accepts
                  it (e.g. to check minimum password length).

                  This can either be a function accepting the input and
                  returning a boolean, or an class reference to a
                  subclass of the prompt toolkit Validator class.

        qmark: Question prefix displayed in front of the question.
               By default this is a ``?``.

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

        multiline: If ``True``, multiline input will be enabled.

        instruction: Write instructions for the user if needed. If ``None``
                     and ``multiline=True``, some instructions will appear.

        lexer: Supply a valid lexer to style the answer. Leave empty to
               use a simple one by default.

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

        kwargs: Additional arguments, they will be passed to prompt toolkit.

    Returns:
        :class:`Question`: Question instance, ready to be prompted (using ``.ask()``).
    """
    merged_style = merge_styles_default([style])
    lexer = lexer or SimpleLexer("class:answer")
    validator = build_validator(validate)

    if instruction is None and multiline:
        instruction = INSTRUCTION_MULTILINE

    def get_prompt_tokens() -> List[Tuple[str, str]]:
        result = [("class:qmark", qmark), ("class:question", " {} ".format(message))]
        if instruction:
            result.append(("class:instruction", " {} ".format(instruction)))
        return result

    bindings = KeyBindings()
    if custom_key_bindings is not None:
        for key, func in custom_key_bindings.items():
            bindings.add(key, eager=True)(func)

    p: PromptSession = PromptSession(
        get_prompt_tokens,
        key_bindings=bindings,
        style=merged_style,
        validator=validator,
        lexer=lexer,
        multiline=multiline,
        **kwargs,
    )
    p.default_buffer.reset(Document(default))

    return Question(p.app)
