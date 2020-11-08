# -*- coding: utf-8 -*-

from typing import Any, Dict, Sequence, Optional, Union

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import Style, merge_styles

from questionary import utils
from questionary.constants import DEFAULT_QUESTION_PREFIX, DEFAULT_STYLE
from questionary.prompts import common
from questionary.prompts.common import Choice, InquirerControl, Separator
from questionary.question import Question


def select(
    message: str,
    choices: Sequence[Union[str, Choice, Dict[str, Any]]],
    default: Optional[Union[str, Choice, Dict[str, Any]]] = None,
    qmark: str = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    use_shortcuts: bool = False,
    use_arrow_keys: bool = True,
    use_indicator: bool = False,
    use_pointer: bool = True,
    instruction: Optional[str] = None,
    **kwargs: Any,
) -> Question:
    """Prompt the user to select one item from the list of choices.

    The user can only select one option.

    Args:
        message: Question text

        choices: Items shown in the selection, this can contain `Choice` or
                 or `Separator` objects or simple items as strings. Passing
                 `Choice` objects, allows you to configure the item more
                 (e.g. preselecting it or disabeling it).

        default: A value corresponding to a selectable item in the choices,
                 to initially set the pointer position to.


        qmark: Question prefix displayed in front of the question.
               By default this is a `?`

        instruction: A hint on how to navigate the menu.
                     It's `(Use shortcuts)` if only `use_shortcuts` is set
                     to True, `(Use arrow keys or shortcuts)` if `use_arrow_keys`
                     & `use_shortcuts` are set and `(Use arrow keys)` by default.

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

        use_indicator: Flag to enable the small indicator in front of the
                       list highlighting the current location of the selection
                       cursor.

        use_shortcuts: Allow the user to select items from the list using
                       shortcuts. The shortcuts will be displayed in front of
                       the list items.

        use_arrow_keys: Allow usage of arrow keys to select item.

        use_pointer: Flag to enable the pointer in front of the currently
                     highlighted element.

    Returns:
        Question: Question instance, ready to be prompted (using `.ask()`).
    """
    if choices is None or len(choices) == 0:
        raise ValueError("A list of choices needs to be provided.")

    if use_shortcuts and len(choices) > len(InquirerControl.SHORTCUT_KEYS):
        raise ValueError(
            "A list with shortcuts supports a maximum of {} "
            "choices as this is the maximum number "
            "of keyboard shortcuts that are available. You"
            "provided {} choices!"
            "".format(len(InquirerControl.SHORTCUT_KEYS), len(choices))
        )

    merged_style = merge_styles([DEFAULT_STYLE, style])

    ic = InquirerControl(
        choices,
        default,
        use_indicator=use_indicator,
        use_shortcuts=use_shortcuts,
        use_arrow_keys=use_arrow_keys,
        use_pointer=use_pointer,
        initial_choice=default,
    )

    def get_prompt_tokens():
        # noinspection PyListCreation
        tokens = [("class:qmark", qmark), ("class:question", " {} ".format(message))]

        if ic.is_answered:
            if isinstance(ic.get_pointed_at().title, list):
                tokens.append(
                    (
                        "class:answer",
                        "".join([token[1] for token in ic.get_pointed_at().title]),
                    )
                )
            else:
                tokens.append(("class:answer", " " + ic.get_pointed_at().title))
        else:
            if instruction:
                tokens.append(("class:instruction", instruction))
            else:
                if use_shortcuts and use_arrow_keys:
                    instruction_msg = " (Use shortcuts or arrow keys)"
                elif use_shortcuts and not use_arrow_keys:
                    instruction_msg = " (Use shortcuts)"
                else:
                    instruction_msg = " (Use arrow keys)"
                tokens.append(("class:instruction", instruction_msg))

        return tokens

    layout = common.create_inquirer_layout(ic, get_prompt_tokens, **kwargs)

    bindings = KeyBindings()

    @bindings.add(Keys.ControlQ, eager=True)
    @bindings.add(Keys.ControlC, eager=True)
    def _(event):
        event.app.exit(exception=KeyboardInterrupt, style="class:aborting")

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

    if use_arrow_keys or use_shortcuts is False:

        @bindings.add(Keys.Down, eager=True)
        @bindings.add("j", eager=True)
        def move_cursor_down(event):
            ic.select_next()
            while not ic.is_selection_valid():
                ic.select_next()

        @bindings.add(Keys.Up, eager=True)
        @bindings.add("k", eager=True)
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

    return Question(
        Application(
            layout=layout,
            key_bindings=bindings,
            style=merged_style,
            **utils.used_kwargs(kwargs, Application.__init__),
        )
    )
