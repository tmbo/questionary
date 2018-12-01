# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from prompt_toolkit.application import Application
from prompt_toolkit.filters import IsDone
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit)
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.shortcuts.prompt import (
    PromptSession)
from prompt_toolkit.styles import merge_styles

from questionary.constants import DEFAULT_STYLE
from questionary.prompts.common import InquirerControl

PY3 = sys.version_info[0] >= 3

if PY3:
    basestring = str


def question(message,
             choices,
             default=None,
             qmark="?",
             style=None,
             **kwargs):
    merged_style = merge_styles([DEFAULT_STYLE, style])

    ic = InquirerControl(choices, default, use_indicator=False)

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", ' {} '.format(message)))
        if ic.answered:
            tokens.append(("class:answer", ' ' + ic.get_pointed_at().title))
        else:
            tokens.append(("class:instruction", ' (Use arrow keys)'))

        return tokens

    ps = PromptSession(get_prompt_tokens, reserve_space_for_menu=0)

    layout = Layout(HSplit([
        ps.layout.container,
        ConditionalContainer(
            Window(ic),
            filter=~IsDone()
        )
    ]))

    bindings = KeyBindings()

    @bindings.add(Keys.ControlQ, eager=True)
    @bindings.add(Keys.ControlC, eager=True)
    def _(event):
        event.app.exit(exception=KeyboardInterrupt, style='class:aborting')

    @bindings.add(Keys.Down, eager=True)
    def move_cursor_down(event):
        ic.select_next()
        while not ic.is_selection_valid():
            ic.select_next()

    @bindings.add(Keys.Up, eager=True)
    def move_cursor_up(event):
        ic.select_previous()
        while not ic.is_selection_valid():
            ic.select_previous()

    @bindings.add(Keys.ControlM, eager=True)
    def set_answer(event):
        ic.answered = True
        event.app.exit(result=ic.get_pointed_at().value)

    @bindings.add(Keys.Any)
    def other(event):
        """Disallow inserting other text. """
        pass

    return Application(
        layout=layout,
        key_bindings=bindings,
        style=merged_style,
        **kwargs
    )
