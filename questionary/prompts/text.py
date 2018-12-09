# -*- coding: utf-8 -*-

from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts.prompt import (
    PromptSession)
from prompt_toolkit.styles import merge_styles, Style
from typing import Text, Type, Union, Callable, Optional, Any

from prompt_toolkit.validation import Validator

from questionary.constants import DEFAULT_STYLE, DEFAULT_QUESTION_PREFIX
from questionary.prompts.common import build_validator
from questionary.question import Question


def text(message: Text,
         qmark: Text = DEFAULT_QUESTION_PREFIX,
         default: Text = "",
         validate: Union[Type[Validator],
                         Callable[[Text], bool],
                         None] = None,  # noqa
         style: Optional[Style] = None,
         **kwargs: Any) -> Question:
    """Prompt the user to enter a free text message."""

    merged_style = merge_styles([DEFAULT_STYLE, style])

    validator = build_validator(validate)

    def get_prompt_tokens():
        return [("class:qmark", qmark),
                ("class:question", ' {} '.format(message))]

    p = PromptSession(get_prompt_tokens,
                      style=merged_style,
                      validator=validator,
                      **kwargs)
    p.default_buffer.reset(Document(default))

    return Question(p.app)
