# -*- coding: utf-8 -*-

from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts.prompt import (
    PromptSession)
from prompt_toolkit.styles import merge_styles

from questionary.constants import DEFAULT_STYLE, DEFAULT_QUESTION_PREFIX
from questionary.prompts.common import build_validator


def question(message,
             qmark=DEFAULT_QUESTION_PREFIX,
             default="",
             validate=None,
             style=None,
             **kwargs):
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

    return p.app
