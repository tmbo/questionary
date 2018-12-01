# -*- coding: utf-8 -*-

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
from questionary.prompts.common import Separator, InquirerControl


def question(message,
             choices,
             default=None,
             qmark="?",
             style=None,
             **kwargs):
    merged_style = merge_styles([DEFAULT_STYLE, style])

    ic = InquirerControl(choices, default)

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", ' {} '.format(message)))
        if ic.answered:
            nbr_selected = len(ic.selected_options)
            if nbr_selected == 0:
                tokens.append(("class:answer", ' done'))
            elif nbr_selected == 1:
                tokens.append(("class:answer",
                               ' [{}]'.format(
                                   ic.get_selected_values()[0].title)))
            else:
                tokens.append(("class:answer",
                               ' done ({} selections)'.format(
                                   nbr_selected)))
        else:
            tokens.append(("class:instruction",
                           ' (Use arrow keys to move, '
                           '<space> to select, '
                           '<a> to toggle, '
                           '<i> to invert)'))
        return tokens

    ps = PromptSession(get_prompt_tokens, reserve_space_for_menu=0, **kwargs)

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
        pointed_choice = ic.get_pointed_at().value
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
            if(not isinstance(c, Separator) and
                    c.value not in ic.selected_options and
                    not c.disabled):
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
