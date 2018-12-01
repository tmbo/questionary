# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
from collections import namedtuple
from typing import List

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
from questionary.prompts.common import setup_simple_validator

PY3 = sys.version_info[0] >= 3

if PY3:
    basestring = str

Choice = namedtuple("Choice", ["title", "value", "disabled"])


class InquirerControl(FormattedTextControl):
    def __init__(self, choices, **kwargs):
        self.selected_option_index = 0
        self.answered = False
        self.choices = []  # type: List[Choice]
        self.selected_options = []  # list of names
        self._init_choices(choices)
        super(InquirerControl, self).__init__(self._get_choice_tokens,
                                              **kwargs)

    def _init_choices(self, choices):
        # helper to convert from question format to internal format
        self.choices = []  # list (name, value, disabled)
        searching_first_choice = True
        for i, c in enumerate(choices):
            if isinstance(c, Separator):
                choice = c
            else:
                if isinstance(c, basestring):
                    choice = Choice(c, c, False)
                else:
                    choice = Choice(c.get('name'),
                                    c.get('value', c.get('name')),
                                    c.get('disabled', None))
                    if c.get('checked') and not choice.disabled:
                        self.selected_options.append(choice.value)

                if searching_first_choice and not choice.disabled:
                    # find the first (available) choice
                    self.selected_option_index = i
                    searching_first_choice = False

            self.choices.append(choice)

    @property
    def choice_count(self):
        return len(self.choices)

    def _get_choice_tokens(self):
        tokens = []

        def append(index, choice):
            selected = (choice.value in self.selected_options)  # use value to check if option has been selected
            pointed_at = (index == self.selected_option_index)

            if pointed_at:
                tokens.append(("class:pointer",
                               ' {} '.format(SELECTED_POINTER)))
                tokens.append(('[SetCursorPosition]', ''))
            else:
                tokens.append(("", '   '))

            if isinstance(choice, Separator):
                tokens.append(("class:separator",
                               "{}".format(choice.title)))
            elif choice.disabled:  # disabled
                tokens.append(("class:selected" if selected else "",
                               '- {} ({})'.format(choice.title, choice.disabled)))
            else:
                if selected:
                    tokens.append(("class:selected", "● {}".format(choice.title)))
                else:
                    tokens.append(("", "○ {}".format(choice.title)))

            tokens.append(("", '\n'))

        # prepare the select choices
        for i, choice in enumerate(self.choices):
            append(i, choice)
        tokens.pop()  # Remove last newline.
        return tokens

    def is_selection_a_separator(self):
        selected = self.choices[self.selected_option_index]
        return isinstance(selected, Separator)

    def is_selection_disabled(self):
        return self.choices[self.selected_option_index].disabled

    def is_selection_valid(self):
        return (not self.is_selection_disabled() and
                not self.is_selection_a_separator())

    def select_previous(self):
        self.selected_option_index = (
                (self.selected_option_index - 1) % self.choice_count)

    def select_next(self):
        self.selected_option_index = (
                (self.selected_option_index + 1) % self.choice_count)

    def get_selection(self):
        return self.choices[self.selected_option_index]

    def get_selected_values(self):
        # get values not labels
        return [c
                for c in self.choices
                if not isinstance(c, Separator) and c.value in self.selected_options]

    @property
    def line_count(self):
        return len(self.choices)


def question(message,
             choices,
             default=0,
             qmark="?",
             style=None,
             **kwargs):
    merged_style = merge_styles([DEFAULT_STYLE, style])

    ic = InquirerControl(choices)
    validator = setup_simple_validator(kwargs)

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", ' {} '.format(message)))
        if ic.answered:
            nbr_selected = len(ic.selected_options)
            if nbr_selected == 0:
                tokens.append(("class:answer", ' done'))
            elif nbr_selected == 1:
                tokens.append(("class:answer", ' [{}]'.format(ic.get_selected_values()[0].title)))
            else:
                tokens.append(("class:answer",
                               ' done ({} selections)'.format(nbr_selected)))
        else:
            tokens.append(("class:instruction",
                           ' (Use arrow keys to move, '
                           '<space> to select, '
                           '<a> to toggle, '
                           '<i> to invert)'))
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

    @bindings.add(' ', eager=True)
    def toggle(event):
        pointed_choice = ic.get_selection().value
        if pointed_choice in ic.selected_options:
            ic.selected_options.remove(pointed_choice)
        else:
            ic.selected_options.append(pointed_choice)

    @bindings.add('i', eager=True)
    def invert(event):
        inverted_selection = [c.value for c in ic.choices if
                              not isinstance(c, Separator) and
                              c.value not in ic.selected_options and
                              not c.disabled]
        ic.selected_options = inverted_selection

    @bindings.add('a', eager=True)
    def all(event):
        all_selected = True  # all choices have been selected
        for c in ic.choices:
            if not isinstance(c, Separator) and c.value not in ic.selected_options and not c.disabled:
                # add missing ones
                ic.selected_options.append(c.value)
                all_selected = False
        if all_selected:
            ic.selected_options = []

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
        event.app.exit(result=[c.value for c in ic.get_selected_values()])

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
