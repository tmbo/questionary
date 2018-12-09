# -*- coding: utf-8 -*-
from typing import Text, List, Optional, Any, Union, Dict

from prompt_toolkit.styles import Style

from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.prompts import select
from questionary.prompts.common import Choice
from questionary.question import Question


def rawselect(message: Text,
              choices: List[Union[Text, Choice, Dict[Text, Any]]],
              default: Optional[Text] = None,
              qmark: Text = DEFAULT_QUESTION_PREFIX,
              style: Optional[Style] = None,
              **kwargs: Any) -> Question:
    return select.select(message, choices, default, qmark, style,
                         use_shortcuts=True,
                         **kwargs)
