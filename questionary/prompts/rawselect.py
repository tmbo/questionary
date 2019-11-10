# -*- coding: utf-8 -*-
from typing import Text, List, Optional, Any, Union, Dict

from prompt_toolkit.styles import Style

from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.prompts import select
from questionary.prompts.common import Choice
from questionary.question import Question


def rawselect(
    message: Text,
    choices: List[Union[Text, Choice, Dict[Text, Any]]],
    default: Optional[Text] = None,
    qmark: Text = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    **kwargs: Any
) -> Question:
    """Ask the user to select one item from a list of choices using shortcuts.

       The user can only select one option.

       Args:
           message: Question text

           choices: Items shown in the selection, this can contain `Choice` or
                    or `Separator` objects or simple items as strings. Passing
                    `Choice` objects, allows you to configure the item more
                    (e.g. preselecting it or disabeling it).

           default: Default return value (single value).

           qmark: Question prefix displayed in front of the question.
                  By default this is a `?`

           style: A custom color and style for the question parts. You can
                  configure colors as well as font types for different elements.

       Returns:
           Question: Question instance, ready to be prompted (using `.ask()`).
       """
    return select.select(
        message, choices, default, qmark, style, use_shortcuts=True, **kwargs
    )
