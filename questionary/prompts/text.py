# -*- coding: utf-8 -*-

from typing import Any, Optional, Text, List, Tuple

from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.lexers import SimpleLexer

from questionary.constants import (
    DEFAULT_QUESTION_PREFIX,
    DEFAULT_STYLE,
    INSTRUCTION_MULTILINE,
)
from questionary.prompts.common import build_validator
from questionary.question import Question


def text(
    message: Text,
    default: Text = "",
    validate: Any = None,
    qmark: Text = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    multiline: bool = False,
    instruction: Optional[Text] = None,
    **kwargs: Any
) -> Question:
    """Prompt the user to enter a free text message.

    This question type can be used to prompt the user for some text input.

    Args:
        message: Question text

        default: Default value will be returned if the user just hits
                 enter.

        validate: Require the entered value to pass a validation. The
                  value can not be submited until the validator accepts
                  it (e.g. to check minimum password length).

                  This can either be a function accepting the input and
                  returning a boolean, or an class reference to a
                  subclass of the prompt toolkit Validator class.

        qmark: Question prefix displayed in front of the question.
               By default this is a `?`

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

        multiline: If `True`, multiline input will be enabled.

        instruction: Write instructions for the user if needed. If `None`
                     and `multiline=True`, some instructions will appear.

    Returns:
        Question: Question instance, ready to be prompted (using `.ask()`).
    """

    merged_style = merge_styles([DEFAULT_STYLE, style])

    validator = build_validator(validate)

    if instruction is None and multiline:
        instruction = INSTRUCTION_MULTILINE

    def get_prompt_tokens() -> List[Tuple[Text, Text]]:
        result = [("class:qmark", qmark), ("class:question", " {} ".format(message))]
        if instruction:
            result.append(("class:instruction", " {} ".format(instruction)))
        return result

    p = PromptSession(
        get_prompt_tokens,
        style=merged_style,
        validator=validator,
        lexer=SimpleLexer("class:answer"),
        multiline=multiline,
        **kwargs,
    )
    p.default_buffer.reset(Document(default))

    return Question(p.app)
