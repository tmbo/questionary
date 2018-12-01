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
from prompt_toolkit.layout import FormattedTextControl, Layout
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit)
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.shortcuts.prompt import (
    PromptSession)
from prompt_toolkit.styles import merge_styles

from questionary.constants import DEFAULT_STYLE, SELECTED_POINTER
from questionary.prompts.common import Separator

PY3 = sys.version_info[0] >= 3

if PY3:
    basestring = str


class InquirerControl(FormattedTextControl):
    def __init__(self, choices, **kwargs):
        self.selected_option_index = 0
        self.answered = False
        self.choices = []
        self._init_choices(choices)
        super(InquirerControl, self).__init__(self._get_choice_tokens,
                                              **kwargs)

    def _init_choices(self, choices, default=None):
        # helper to convert from question format to internal format
        self.choices = []  # list (name, value, disabled)
        searching_first_choice = True
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                self.choices.append((c, None, None))
            else:
                if isinstance(c, basestring):
                    self.choices.append((c, c, None))
                else:
                    name = c.get('name')
                    value = c.get('value', name)
                    disabled = c.get('disabled', None)
                    self.choices.append((name, value, disabled))
                if searching_first_choice:
                    self.selected_option_index = i  # found the first choice
                    searching_first_choice = False

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index, choice):
            pointed_at = (index == self.selected_option_index)

            if pointed_at:
                tokens.append(("class:pointer",
                               ' {} '.format(SELECTED_POINTER)))
                tokens.append(('[SetCursorPosition]', ''))
            else:
                tokens.append(("", '   '))

            if isinstance(choice[0], Separator):
                tokens.append(("class:separator",
                               "{}".format(choice[0])))
            elif choice[2]:  # disabled
                tokens.append(("class:selected" if pointed_at else "",
                               '- {} ({})'.format(choice[0], choice[2])))
            else:
                tokens.append(("class:selected" if pointed_at else "",
                               "{}".format(choice[0])))
            tokens.append(("", '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()  # Remove last newline.
        return tokens

    def is_selection_a_separator(self):
        selected = self.choices[self.selected_option_index]
        return isinstance(selected[0], Separator)

    def is_selection_disabled(self):
        return self.choices[self.selected_option_index][2]

    def is_selection_valid(self):
        return (not self.is_selection_disabled() and
                not self.is_selection_a_separator())

    def select_next(self):
        self.selected_option_index = (
            (self.selected_option_index - 1) % self.choice_count)

    def select_previous(self):
        self.selected_option_index = (
            (self.selected_option_index + 1) % self.choice_count)

    def get_selection(self):
        return self.choices[self.selected_option_index]


def question(message,
             choices,
             default=0,
             qmark="?",
             style=None,
             **kwargs):
    merged_style = merge_styles([DEFAULT_STYLE, style])

    ic = InquirerControl(choices)

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", ' {} '.format(message)))
        if ic.answered:
            tokens.append(("class:answer", ' ' + ic.get_selection()[0]))
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
        ic.select_previous()
        while not ic.is_selection_valid():
            ic.select_previous()

    @bindings.add(Keys.Up, eager=True)
    def move_cursor_up(event):
        ic.select_next()
        while not ic.is_selection_valid():
            ic.select_next()

    @bindings.add(Keys.ControlM, eager=True)
    def set_answer(event):
        ic.answered = True
        event.app.exit(result=ic.get_selection()[1])

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
