# -*- coding: utf-8 -*-
"""
`list` type question
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import inspect

from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts.prompt import (
    PromptSession)
from prompt_toolkit.styles import merge_styles
from prompt_toolkit.validation import Validator, ValidationError

from questionary.constants import DEFAULT_STYLE


def question(message,
             qmark="?",
             default="",
             validate=None,
             style=None,
             **kwargs):
    merged_style = merge_styles([DEFAULT_STYLE, style])
    validator = None

    if validate:
        if inspect.isclass(validate) and issubclass(validate, Validator):
            validator = validate()
        elif callable(validate):
            class _InputValidator(Validator):
                def validate(self, document):
                    verdict = validate(document.text)
                    if verdict is not True:
                        if verdict is False:
                            verdict = 'invalid input'
                        raise ValidationError(
                            message=verdict,
                            cursor_position=len(document.text))

            validator = _InputValidator()

    def get_prompt_tokens():
        return [("class:qmark", qmark),
                ("class:question", ' {} '.format(message))]

    p = PromptSession(get_prompt_tokens,
                      style=merged_style,
                      validator=validator,
                      **kwargs)
    p.default_buffer.reset(Document(default))

    return p.app
