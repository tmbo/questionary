# -*- coding: utf-8 -*-
from typing import Text, Type, Union, Callable, Optional, Any

from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator

from questionary.question import Question
from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.prompts import text


def password(message: Text,
             qmark: Text = DEFAULT_QUESTION_PREFIX,
             default: Text = "",
             validate: Union[Type[Validator],
                             Callable[[Text], bool],
                             None] = None,
             style: Optional[Style] = None,
             **kwargs: Any) -> Question:
    return text.text(message, qmark, default, validate, style,
                     is_password=True, **kwargs)
