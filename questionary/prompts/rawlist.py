# -*- coding: utf-8 -*-

from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.prompts import list


def question(message,
             choices,
             default=None,
             qmark=DEFAULT_QUESTION_PREFIX,
             style=None,
             **kwargs):
    return list.question(message, choices, default, qmark, style,
                         use_shortcuts=True,
                         **kwargs)
