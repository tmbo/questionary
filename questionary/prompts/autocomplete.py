# -*- coding: utf-8 -*-
from typing import Any, Optional, Text, List, Dict

from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit.styles import merge_styles, Style

from questionary.constants import DEFAULT_STYLE, DEFAULT_QUESTION_PREFIX
from prompt_toolkit.document import Document
from questionary.prompts.common import build_validator
from questionary.question import Question

from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML


class QuestionaryCompleter(Completer):
    def __init__(self, words, ignore_case=True, meta_dict=None,
                 sentence=True, match_middle=True):

        self.words = words
        self.ignore_case = ignore_case
        self.meta_dict = meta_dict or {}
        self.sentence = sentence
        self.match_middle = match_middle

    def get_completions(self, document, complete_event):
        words = self.words
        if callable(words):
            words = words()

        # Get word/text before cursor.
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor()

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def word_matches(word):
            """Match index if found, -1 if not. """
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return word.find(word_before_cursor)
            else:
                return 0 if word.startswith(word_before_cursor) else -1

        for word in words:
            index = word_matches(word)
            if index != -1:
                display_meta = self.meta_dict.get(word, '')
                display = HTML('%s<b><u>%s</u></b>%s') % \
                    (word[:index], word[index:index + len(word_before_cursor)],
                     word[index + len(word_before_cursor):len(word)])

                yield Completion(
                    word,
                    start_position=-len(word),
                    display=display,
                    display_meta=display_meta,
                    style='class:answer',
                    selected_style='class:selected')


def autocomplete(message: Text,
                 choices: List[Text] = None,
                 default: Optional[Text] = "",
                 qmark: Text = DEFAULT_QUESTION_PREFIX,
                 completer: Completer = QuestionaryCompleter,
                 meta_dict: Dict = None,
                 ignore_case: bool = True,
                 match_middle: bool = True,
                 complete_style: Text = 'COLUMN',
                 validate: Any = None,
                 style: Optional[Style] = None,
                 **kwargs: Any) -> Question:
    """Prompt the user to enter a message with autocomplete help.

    Args:
        message: Question text

        choices: Items shown in the selection, this contains items as strings

        default: Default return value (single value).

        qmark: Question prefix displayed in front of the question.
               By default this is a `?`

        completer: A Subclass of Completer prompt_toolkit. If default not used,
                   style wont work.

        meta_dict: A dictionary with information/anything about choices.

        ignore_case: If true autocomplete would ignore case.

        match_middle: If true autocomplete would search in every string position
                      not only in string begin.

        complete_style: How autocomplete menu would be shown, it could be
                        COLUMN, MULTI_COLUMN or READLINE_LIKE

        validate: Require the entered value to pass a validation. The
                  value can not be submited until the validator accepts
                  it (e.g. to check minimum password length).

                  This can either be a function accepting the input and
                  returning a boolean, or an class reference to a
                  subclass of the prompt toolkit Validator class.

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

    Returns:
        Question: Question instance, ready to be prompted (using `.ask()`).
    """
    if choices is None or len(choices) == 0:
        raise ValueError('No choices is given, you should use Text question.')
    if completer is not QuestionaryCompleter and style:
        print("It is possible that style would not be used.")

    merged_style = merge_styles([DEFAULT_STYLE, style])

    def get_prompt_tokens():
        tokens = [("class:qmark", qmark),
                  ("class:question", ' {} '.format(message))]

        return tokens

    def get_meta_style(meta_dict):
        if meta_dict:
            for key in meta_dict:
                meta_dict[key] = HTML(f"<text>{meta_dict[key]}</text>")

        return meta_dict

    validator = build_validator(validate)
    my_completer = completer(choices, meta_dict=get_meta_style(meta_dict),
                             ignore_case=ignore_case, match_middle=match_middle)
    p = PromptSession(
        get_prompt_tokens,
        style=merged_style,
        completer=my_completer,
        validator=validator,
        complete_style=complete_style,
        **kwargs
    )
    p.default_buffer.reset(Document(default))

    return Question(p.app)
