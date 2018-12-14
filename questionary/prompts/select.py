# -*- coding: utf-8 -*-
from typing import Any, Optional, Text, List, Union, Dict

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
from prompt_toolkit.styles import merge_styles, Style

from questionary.constants import DEFAULT_STYLE, DEFAULT_QUESTION_PREFIX
from questionary.prompts.common import InquirerControl, Separator, Choice
from questionary.question import Question


def select(message: Text,
           choices: List[Union[Text, Choice, Dict[Text, Any]]],
           default: Optional[Text] = None,
           qmark: Text = DEFAULT_QUESTION_PREFIX,
           style: Optional[Style] = None,
           use_shortcuts: bool = False,
           use_indicator: bool = False,
           **kwargs: Any) -> Question:
    """Prompt the user to select one item from the list of choices.

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

        use_indicator: Flag to enable the small indicator in front of the
                       list highlighting the current location of the selection
                       cursor.

        use_shortcuts: Allow the user to select items from the list using
                       shortcuts. The shortcuts will be displayed in front of
                       the list items.
    Returns:
        Question: Question instance, ready to be prompted (using `.ask()`).
    """

    if use_shortcuts and len(choices) > len(InquirerControl.SHORTCUT_KEYS):
        raise ValueError('A list with shortcuts supports a maximum of {} '
                         'choices as this is the maximum number '
                         'of keyboard shortcuts that are available. You'
                         'provided {} choices!'
                         ''.format(len(InquirerControl.SHORTCUT_KEYS),
                                   len(choices)))

    merged_style = merge_styles([DEFAULT_STYLE, style])

    ic = InquirerControl(choices, default,
                         use_indicator=use_indicator,
                         use_shortcuts=use_shortcuts)

    def get_prompt_tokens():
        # noinspection PyListCreation
        tokens = [("class:qmark", qmark),
                  ("class:question", ' {} '.format(message))]

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

            # noinspection PyShadowingNames
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

    return Question(Application(
        layout=layout,
        key_bindings=bindings,
        style=merged_style,
        **kwargs
    ))
