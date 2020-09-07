# -*- coding: utf-8 -*-

from prompt_toolkit.styles import Style

# Value to display as an answer when "affirming" a confirmation question
YES = "Yes"

# Value to display as an answer when "denying" a confirmation question
NO = "No"

# Instruction text for a confirmation question (yes is default)
YES_OR_NO = "(Y/n)"

# Instruction text for a confirmation question (no is default)
NO_OR_YES = "(y/N)"

# Selection token used to indicate the selection cursor in a list
SELECTED_POINTER = "»"

# Item prefix to identify selected items in a checkbox list
INDICATOR_SELECTED = "●"

# Item prefix to identify unselected items in a checkbox list
INDICATOR_UNSELECTED = "○"

# Prefix displayed in front of questions
DEFAULT_QUESTION_PREFIX = "?"

# Message shown when a user aborts a question prompt using CTRL-C
DEFAULT_KBI_MESSAGE = "Cancelled by user"

# Default message style
DEFAULT_STYLE = Style(
    [
        ("qmark", "fg:#5f819d"),  # token in front of the question
        ("question", "bold"),  # question text
        ("answer", "fg:#FF9D00 bold"),  # submitted answer text behind the question
        ("pointer", ""),  # pointer used in select and checkbox prompts
        ("selected", ""),  # style for a selected item of a checkbox
        ("separator", ""),  # separator in lists
        ("instruction", ""),  # user instructions for select, rawselect, checkbox
    ]
)
