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

from questionary.constants import DEFAULT_STYLE, DEFAULT_QUESTION_PREFIX
from questionary.prompts.common import InquirerControl, Separator


def question(message,
             choices,
             default=None,
             qmark=DEFAULT_QUESTION_PREFIX,
             style=None,
             use_shortcuts=False,
             use_indicator=False,
             **kwargs):

    if use_shortcuts and len(choices) > len(InquirerControl.SHORTCUT_KEYS):
        raise ValueError('A list with shortcuts supports a maximum of '
                         f'{len(InquirerControl.SHORTCUT_KEYS)} '
                         'choices as this is the maximum number '
                         'of keyboard shortcuts that are available. You'
                         f'provided {len(choices)} choices!')

    merged_style = merge_styles([DEFAULT_STYLE, style])

    ic = InquirerControl(choices, default,
                         use_indicator=use_indicator,
                         use_shortcuts=use_shortcuts)

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", ' {} '.format(message)))
        if ic.is_answered:
            tokens.append(("class:answer", ' ' + ic.get_pointed_at().title))
        else:
            if use_shortcuts:
                tokens.append(("class:instruction", ' (Use shortcuts)'))
            else:
                tokens.append(("class:instruction", ' (Use arrow keys)'))

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

    if use_shortcuts:
        # add key bindings for choices
        for i, c in enumerate(ic.choices):
            if isinstance(c, Separator):
                continue

            def _reg_binding(i, keys):
                # trick out late evaluation with a "function factory":
                # https://stackoverflow.com/a/3431699
                @bindings.add(keys, eager=True)
                def select_choice(event):
                    ic.pointed_at = i

            _reg_binding(i, c.shortcut_key)
    else:
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
        ic.is_answered = True
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
