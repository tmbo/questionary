# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import (
    to_formatted_text)
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import merge_styles

from questionary.constants import NO_OR_YES, YES, NO, YES_OR_NO, DEFAULT_STYLE


def question(message,
             qmark="?",
             default=True,
             style=None,
             **kwargs):
    """Create a `PromptSession` object for the 'confirm' function."""

    merged_style = merge_styles([DEFAULT_STYLE, style])

    status = {'answer': None}

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", ' {} '.format(message)))

        if status['answer'] is not None:
            answer = ' {}'.format(YES if status['answer'] else NO)
            tokens.append(("class:answer", answer))
        else:
            instruction = ' {}'.format(YES_OR_NO if default else NO_OR_YES)
            tokens.append(("class:instruction", instruction))

        return to_formatted_text(tokens)

    bindings = KeyBindings()

    @bindings.add(Keys.ControlQ, eager=True)
    @bindings.add(Keys.ControlC, eager=True)
    def _(event):
        event.app.exit(exception=KeyboardInterrupt, style='class:aborting')

    @bindings.add('n')
    @bindings.add('N')
    def key_n(event):
        status['answer'] = False
        event.app.exit(result=False)

    @bindings.add('y')
    @bindings.add('Y')
    def key_y(event):
        status['answer'] = True
        event.app.exit(result=True)

    @bindings.add(Keys.ControlM, eager=True)
    def set_answer(event):
        status['answer'] = default
        event.app.exit(result=default)

    @bindings.add(Keys.Any)
    def other(event):
        """Disallow inserting other text."""
        pass

    return PromptSession(get_prompt_tokens,
                         key_bindings=bindings,
                         style=merged_style,
                         **kwargs).app
