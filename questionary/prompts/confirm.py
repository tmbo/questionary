from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.styles import merge_styles, Style
from typing import Optional, Any

from questionary.constants import (
    NO_OR_YES,
    YES,
    NO,
    YES_OR_NO,
    DEFAULT_STYLE,
    DEFAULT_QUESTION_PREFIX,
)
from questionary.question import Question


def confirm(
    message: str,
    default: bool = True,
    qmark: str = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    **kwargs: Any,
) -> Question:
    """Prompt the user to confirm or reject.

    This question type can be used to prompt the user for a confirmation
    of a yes-or-no question. If the user just hits enter, the default
    value will be returned.

    Args:
        message: Question text

        default: Default value will be returned if the user just hits
                 enter.

        qmark: Question prefix displayed in front of the question.
               By default this is a `?`

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

    Returns:
        Question: Question instance, ready to be prompted (using `.ask()`).
    """

    merged_style = merge_styles([DEFAULT_STYLE, style])

    status = {"answer": None}

    def get_prompt_tokens():
        tokens = []

        tokens.append(("class:qmark", qmark))
        tokens.append(("class:question", " {} ".format(message)))

        if status["answer"] is not None:
            answer = " {}".format(YES if status["answer"] else NO)
            tokens.append(("class:answer", answer))
        else:
            instruction = " {}".format(YES_OR_NO if default else NO_OR_YES)
            tokens.append(("class:instruction", instruction))

        return to_formatted_text(tokens)

    bindings = KeyBindings()

    @bindings.add(Keys.ControlQ, eager=True)
    @bindings.add(Keys.ControlC, eager=True)
    def _(event):
        event.app.exit(exception=KeyboardInterrupt, style="class:aborting")

    @bindings.add("n")
    @bindings.add("N")
    def key_n(event):
        status["answer"] = False
        event.app.exit(result=False)

    @bindings.add("y")
    @bindings.add("Y")
    def key_y(event):
        status["answer"] = True
        event.app.exit(result=True)

    @bindings.add(Keys.ControlM, eager=True)
    def set_answer(event):
        status["answer"] = default
        event.app.exit(result=default)

    @bindings.add(Keys.Any)
    def other(event):
        """Disallow inserting other text."""
        pass

    return Question(
        PromptSession(
            get_prompt_tokens, key_bindings=bindings, style=merged_style, **kwargs
        ).app
    )
