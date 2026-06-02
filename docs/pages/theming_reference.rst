.. _theming-styling-reference:

*******************************
Theming & Styling Reference
*******************************

This  reference documents all style tokens used by questionary prompts, including which tokens each question type uses and how to override them.
This is in addition to the overview provided in :ref:`advanced-themes-styling`.

This page is up to date for questionary version : 2.1.1.
Later / future versions may introduce new tokens or change defaults, so you may need check the source code for the most current information.

Overview
########

What are styles?
****************

In questionary, styles are ``prompt_toolkit.styles.Style`` objects created from a list of 2-tuples like ``[("qmark", "fg:#673ab7 bold"), ("question", "bold")]``. Each tuple maps a **token name** (the style class) to a **prompt_toolkit style string** (colors, bold, italic, etc.).

How styles work
***************

When rendering a prompt, questionary emits formatted text with class names like ``("class:qmark", "?")`` or ``("class:answer", "user input")``. The Style object maps these class names to visual styles. Questionary uses the prefix ``"class:"`` internally, but you define styles without it: just ``("qmark", "...")``.

Style application
*****************

- Every prompt function accepts a ``style=`` parameter
- Your custom style is merged with ``DEFAULT_STYLE`` using ``merge_styles_default()`` (source: ``questionary/styles.py``)
- Custom styles **override** matching tokens in the default style
- Merging order: ``DEFAULT_STYLE`` → user style → prompt_toolkit merge

Recognized token names
**********************

**Questionary-specific tokens** recognized across questionary prompts:

``qmark``, ``question``, ``answer``, ``instruction``, ``pointer``, ``highlighted``, ``selected``, ``separator``, ``text``, ``disabled``, ``search_success``, ``search_none``, ``question-mark``, ``validation-toolbar``, ``bottom-toolbar``

**Prompt_toolkit tokens** inherited from the underlying UI framework (see the "Prompt Toolkit Style Tokens" section for complete list):

Completion menus: ``completion-menu``, ``completion-menu.completion``, ``completion-menu.completion.current``, ``completion-menu.meta.completion``, and various fuzzymatch tokens

Scrollbars: ``scrollbar.background``, ``scrollbar.button``, ``scrollbar.arrow``

Toolbars: ``completion-toolbar``, ``search-toolbar``, ``system-toolbar``, ``arg-toolbar``

UI elements: ``selected``, ``cursor-line``, ``cursor-column``, ``matching-bracket``, ``line-number``, ``auto-suggestion``, ``trailing-whitespace``, ``aborting``, ``exiting``

You can style any of these tokens in your custom Style object.

Default Style
#############

Defined in ``questionary/constants.py`` as ``DEFAULT_STYLE``:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Token
     - Default Style String
     - Description
   * - ``qmark``
     - ``fg:#5f819d``
     - Blue-gray color for question mark prefix
   * - ``question``
     - ``bold``
     - Bold formatting for question text
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - Orange bold for submitted answers
   * - ``search_success``
     - ``noinherit fg:#00FF00 bold``
     - Green for successful search matches
   * - ``search_none``
     - ``noinherit fg:#FF0000 bold``
     - Red when search finds nothing
   * - ``pointer``
     - ``""`` (empty)
     - Unstyled - uses terminal default
   * - ``selected``
     - ``""`` (empty)
     - Unstyled
   * - ``separator``
     - ``""`` (empty)
     - Unstyled
   * - ``instruction``
     - ``""`` (empty)
     - Unstyled
   * - ``text``
     - ``""`` (empty)
     - Unstyled

Tokens NOT in default style
****************************

The following tokens render with terminal defaults: ``highlighted``, ``disabled``, ``question-mark``, ``validation-toolbar``, ``bottom-toolbar``


In addition to questionary-specific tokens, you can style any prompt_toolkit UI element. These tokens are inherited from prompt_toolkit's default UI style and control various interface components:


Creating Custom Styles
#######################

Creating a custom style
***********************

.. code-block:: python3

   from questionary import Style

   custom = Style([
       ("qmark", "fg:#673ab7 bold"),      # Purple question mark
       ("answer", "fg:#f44336 bold"),      # Red answer text
   ])

Passing style to a prompt
**************************

.. code-block:: python3

   import questionary

   result = questionary.text("Your name?", style=custom).ask()

How merging works
*****************

- Base layer: ``DEFAULT_STYLE`` 
- Your style overwrites matching tokens only
- Unspecified tokens keep their defaults

Question Types
##############

text
****

**What renders:** Single-line text input with prefix, question text, optional instruction, and user's typed input.

**Source:** ``questionary/prompts/text.py``

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``qmark``
     - ``fg:#5f819d``
     - The ``?`` prefix symbol before the question
     - Always
     - ``("qmark", "fg:#00afff bold")``
   * - ``question``
     - ``bold``
     - The question message text itself
     - Always
     - ``("question", "fg:#ffffff")``
   * - ``instruction``
     - ``""``
     - Hint text (e.g., multiline instructions)
     - When ``instruction=`` provided
     - ``("instruction", "fg:#888 italic")``
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - User's typed input as they type
     - While typing
     - ``("answer", "fg:#00d700")``
   * - ``cursor-line``
     - [Prompt toolkit]
     - Current line highlighting
     - During text editing
     - See "Other UI Tokens"
   * - ``cursor-column``
     - [Prompt toolkit]
     - Current column highlighting
     - During text editing
     - See "Other UI Tokens"
   * - ``auto-suggestion``
     - [Prompt toolkit]
     - Auto-suggestion text
     - When suggestions available
     - See "Other UI Tokens"

See the "Prompt Toolkit Style Tokens" section for complete details and default values.

Visual layout::

    [qmark] [question] [instruction]
    [answer...]

Example:

.. code-block:: python3

   questionary.text(
       "Your name?",
       instruction="(required)",
       style=Style([("answer", "fg:#00ff00")])
   ).ask()

password
********

**What renders:** Same as ``text`` but input is masked with ``*`` characters. Internally delegates to ``text(..., is_password=True)`` (source: ``questionary/prompts/password.py``).

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``qmark``
     - ``fg:#5f819d``
     - The ``?`` prefix
     - Always
     - ``("qmark", "fg:#ff0000 bold")``
   * - ``question``
     - ``bold``
     - Question message
     - Always
     - ``("question", "underline")``
   * - ``instruction``
     - ``""``
     - Optional hint
     - If provided
     - ``("instruction", "fg:#666")``
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - Masked input (``***``)
     - While typing
     - ``("answer", "fg:#ff5f00")``
   * - ``cursor-line``
     - [Prompt toolkit]
     - Current line highlighting
     - During text editing
     - See "Other UI Tokens"
   * - ``cursor-column``
     - [Prompt toolkit]
     - Current column highlighting
     - During text editing
     - See "Other UI Tokens"
   * - ``auto-suggestion``
     - [Prompt toolkit]
     - Auto-suggestion text
     - When suggestions available
     - See "Other UI Tokens"

See the "Prompt Toolkit Style Tokens" section for complete details and default values.

confirm
*******

**What renders:** Yes/no question with ``(Y/n)`` or ``(y/N)`` prompt, accepts y/n keys, displays final answer.

**Source:** ``questionary/prompts/confirm.py``

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``qmark``
     - ``fg:#5f819d``
     - The ``?`` prefix
     - Always
     - ``("qmark", "fg:#00d700")``
   * - ``question``
     - ``bold``
     - Question text
     - Always
     - ``("question", "bold underline")``
   * - ``instruction``
     - ``""``
     - The ``(Y/n)`` or ``(y/N)`` hint
     - Before answer
     - ``("instruction", "fg:#666")``
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - Final ``Yes`` or ``No``
     - After submission
     - ``("answer", "fg:#00ff00 bold")``

Visual layout::

    [qmark] [question] [instruction]    →   [qmark] [question] [answer]
    ?       Continue?   (Y/n)                ?       Continue?   Yes

select
******

**What renders:** Scrollable list of choices with arrow/pointer indicating current position. User navigates with arrow keys or shortcuts.

**Source:** ``questionary/prompts/select.py`` (header), ``questionary/prompts/common.py`` (list items)

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``qmark``
     - ``fg:#5f819d``
     - The ``?`` prefix
     - Always
     - ``("qmark", "fg:#5fafff bold")``
   * - ``question``
     - ``bold``
     - Question text
     - Always
     - ``("question", "fg:#ffffff bold")``
   * - ``instruction``
     - ``""``
     - Navigation hint (e.g., "Use arrow keys")
     - Before selection
     - ``("instruction", "italic")``
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - Selected choice after submission
     - After selection
     - ``("answer", "fg:#00d700 bold")``
   * - ``pointer``
     - ``""``
     - The ``»`` arrow next to current choice
     - Always (in list)
     - ``("pointer", "fg:#ff9d00 bold")``
   * - ``highlighted``
     - (not in default)
     - The currently focused/pointed-at choice
     - Current item
     - ``("highlighted", "fg:#00afff bold")``
   * - ``text``
     - ``""``
     - Non-highlighted choice text
     - Other items
     - ``("text", "fg:#cccccc")``
   * - ``separator``
     - ``""``
     - Separator line items
     - When Separator() used
     - ``("separator", "fg:#666")``
   * - ``disabled``
     - (not in default)
     - Disabled choice with explanation
     - Disabled items
     - ``("disabled", "fg:#888 italic")``
   * - ``scrollbar.*``
     - [Prompt toolkit]
     - Scrollbar appearance in choice list
     - When list exceeds viewport
     - See "Scrollbar Tokens"

See the "Prompt Toolkit Style Tokens" section for complete details and default values.

Visual layout::

    [qmark] [question] [instruction]
      [pointer] [highlighted]choice A
                [text]choice B
                [text]choice C

select with search filter
-------------------------

When ``use_search_filter=True`` is enabled:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Additional Token
     - Default Style
     - What It Controls
   * - ``question-mark``
     - (not in default)
     - The ``/`` and ``...`` in search line
   * - ``search_success``
     - ``noinherit fg:#00FF00 bold``
     - Search text when matches found
   * - ``search_none``
     - ``noinherit fg:#FF0000 bold``
     - Search text when no matches

rawselect
*********

**What renders:** Same as ``select`` but with mandatory keyboard shortcuts (``1)``, ``2)``, etc.) and no arrow key navigation.

**Implementation:** Calls ``select(..., use_shortcuts=True, use_arrow_keys=False)`` (source: ``questionary/prompts/rawselect.py``)

**Token usage:** Identical to ``select`` above. All same tokens apply.

checkbox
********

**What renders:** Multi-select list with checkboxes (``○``/``●``), allows toggling multiple items, validates before submission.

**Source:** ``questionary/prompts/checkbox.py`` (header), ``questionary/prompts/common.py`` (list)

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``qmark``
     - ``fg:#5f819d``
     - The ``?`` prefix
     - Always
     - ``("qmark", "fg:#d75f00 bold")``
   * - ``question``
     - ``bold``
     - Question text
     - Always
     - ``("question", "fg:#ffffff bold")``
   * - ``instruction``
     - ``""``
     - Hint text (space/toggle/keys)
     - Before submission
     - ``("instruction", "fg:#666")``
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - Summary (``done``, ``done (2 selections)``, ``[itemname]``)
     - After submission
     - ``("answer", "fg:#5faf00 bold")``
   * - ``pointer``
     - ``""``
     - The ``»`` next to current item
     - Always (in list)
     - ``("pointer", "fg:#00afff bold")``
   * - ``highlighted``
     - (not in default)
     - Currently focused item text
     - Current position
     - ``("highlighted", "fg:#00d7ff bold")``
   * - ``selected``
     - ``""``
     - Checked item text and ``●`` indicator
     - Checked items
     - ``("selected", "fg:#00d700")``
   * - ``text``
     - ``""``
     - Unchecked item text and ``○`` indicator
     - Unchecked items
     - ``("text", "fg:#aaaaaa")``
   * - ``separator``
     - ``""``
     - Separator lines
     - When Separator() used
     - ``("separator", "fg:#555")``
   * - ``disabled``
     - (not in default)
     - Disabled items with reason
     - Disabled items
     - ``("disabled", "fg:#666 italic")``
   * - ``validation-toolbar``
     - (not in default)
     - Error message when validation fails
     - Invalid submission
     - ``("validation-toolbar", "fg:#fff bg:#d70000")``
   * - ``bottom-toolbar``
     - (not in default)
     - Container for validation message
     - With validation error
     - ``("bottom-toolbar", "noreverse")``
   * - ``scrollbar.*``
     - [Prompt toolkit]
     - Scrollbar appearance in choice list
     - When list exceeds viewport
     - See "Scrollbar Tokens"

See the "Prompt Toolkit Style Tokens" section for complete details and default values.

Visual layout::

    [qmark] [question] [instruction]
      [pointer] [selected/text]○/● [highlighted/selected/text]choice
                [text]○ choice
                [text]○ choice

    [validation-toolbar]Error message here (if validation fails)

.. note::

   ``checkbox`` adds ``Style([("bottom-toolbar", "noreverse")])`` before user style to disable default inversion (source: ``questionary/prompts/checkbox.py:147``).

autocomplete
************

**What renders:** Text input with dropdown completion menu showing filtered suggestions as you type.

**Source:** ``questionary/prompts/autocomplete.py`` (prompt), ``92-99`` (completion items)

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``qmark``
     - ``fg:#5f819d``
     - The ``?`` prefix
     - Always
     - ``("qmark", "fg:#5f87ff bold")``
   * - ``question``
     - ``bold``
     - Question text
     - Always
     - ``("question", "fg:#ffffff")``
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - User's typed input text
     - While typing
     - ``("answer", "fg:#87afff")``
   * - ``selected``
     - ``""``
     - Highlighted completion in dropdown
     - Completion menu
     - ``("selected", "fg:#000 bg:#87afff")``
   * - ``completion-menu.*``
     - [Prompt toolkit]
     - Dropdown menu styling (background, current item, meta info, fuzzy matching)
     - During autocompletion
     - See "Completion Menu Tokens"
   * - ``scrollbar.*``
     - [Prompt toolkit]
     - Scrollbar in completion dropdown
     - When suggestions exceed viewport
     - See "Scrollbar Tokens"
   * - ``cursor-line``
     - [Prompt toolkit]
     - Current line highlighting
     - During text editing
     - See "Other UI Tokens"
   * - ``cursor-column``
     - [Prompt toolkit]
     - Current column highlighting
     - During text editing
     - See "Other UI Tokens"

See the "Prompt Toolkit Style Tokens" section for complete details and default values. See the "Example: Custom Completion Menu Style" section at the end for a complete working example.

.. note::

   Completion items use ``style="class:answer"`` and ``selected_style="class:selected"`` in the completer (source: line 97-98). The dropdown menu styling uses prompt_toolkit's completion UI.

path
****

**What renders:** Text input with filesystem path autocompletion, automatically suggests directories/files.

**Source:** ``questionary/prompts/path.py``

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``qmark``
     - ``fg:#5f819d``
     - The ``?`` prefix
     - Always
     - ``("qmark", "fg:#00af87 bold")``
   * - ``question``
     - ``bold``
     - Question text
     - Always
     - ``("question", "fg:#ffffff")``
   * - ``answer``
     - ``fg:#FF9D00 bold``
     - Typed path text
     - While typing
     - ``("answer", "fg:#87ff00")``
   * - ``completion-menu.*``
     - [Prompt toolkit]
     - Dropdown menu for file/directory suggestions
     - During path completion
     - See "Completion Menu Tokens"
   * - ``scrollbar.*``
     - [Prompt toolkit]
     - Scrollbar in completion dropdown
     - When suggestions exceed viewport
     - See "Scrollbar Tokens"
   * - ``cursor-line``
     - [Prompt toolkit]
     - Current line highlighting
     - During text editing
     - See "Other UI Tokens"
   * - ``cursor-column``
     - [Prompt toolkit]
     - Current column highlighting
     - During text editing
     - See "Other UI Tokens"

See the "Prompt Toolkit Style Tokens" section for complete details and default values. Like ``autocomplete``, the ``path`` prompt displays a dropdown with file/directory suggestions.

.. note::

   Uses ``SimpleLexer("class:answer")`` for input styling. Path completion UI is handled by prompt_toolkit's ``PathCompleter``.

press_any_key_to_continue
**************************

**What renders:** Simple message that waits for any keypress. No question mark, no complex input.

**Source:** ``questionary/prompts/press_any_key_to_continue.py``

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``question``
     - ``bold``
     - The message text
     - Always
     - ``("question", "fg:#00afff")``

Visual layout::

    [question]Press any key to continue...

.. note::

   This is the only prompt that does NOT use ``qmark``, ``answer``, or ``instruction``.

print
*****

**What renders:** Static text output, not a question. Uses ``prompt_toolkit.print_formatted_text``.

**Source:** ``questionary/prompts/common.py``

**Token usage:**

.. list-table::
   :header-rows: 1
   :widths: 15 20 30 15 20

   * - Token
     - Default Style
     - What It Controls
     - When Visible
     - Override Example
   * - ``text``
     - ``""``
     - All printed text
     - Always
     - Pass as string: ``style="fg:#ff5f00 bold"``

.. note::

   If ``style=`` is a string (not a Style object), questionary wraps it as ``Style([("text", style)])``. Otherwise uses ``DEFAULT_STYLE``.

Example:

.. code-block:: python3

   questionary.print("Hello!", style="fg:#00ff00 bold italic")

form
****

**What renders:** Sequential execution of multiple question prompts. Not a unique prompt type - just a container.

**Token usage:** None directly. Each child question uses its own style.

Example:

.. code-block:: python3

   form = questionary.form(
       name=questionary.text("Name?", style=Style([("answer", "fg:#00ff00")])),
       confirm=questionary.confirm("OK?", style=Style([("answer", "fg:#ff0000")])),
   )
   results = form.ask()

Token Cross-Reference
#####################

This table shows which tokens are used by each question type:

.. list-table::

   * - Question Type
     - qmark
     - question
     - answer
     - instruction
     - pointer
     - highlighted
     - selected
     - text
     - separator
     - disabled
     - search†
     - validation‡
     - scrollbar.*
     - completion-menu.*
     - cursor-*
   * - **text**
     - ✓
     - ✓
     - ✓
     - ✓
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - ✓
   * - **password**
     - ✓
     - ✓
     - ✓
     - ✓
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - ✓
   * - **confirm**
     - ✓
     - ✓
     - ✓
     - ✓
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - **select**
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - 
     - ✓
     - ✓
     - ✓
     - ✓*
     - 
     - ✓*
     - 
     - 
   * - **rawselect**
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - 
     - ✓
     - ✓
     - ✓
     - ✓*
     - 
     - ✓*
     - 
     - 
   * - **checkbox**
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓*
     - ✓
     - ✓*
     - 
     - 
   * - **autocomplete**
     - ✓
     - ✓
     - ✓
     - 
     - 
     - 
     - ✓
     - 
     - 
     - 
     - 
     - 
     - ✓*
     - ✓
     - ✓
   * - **path**
     - ✓
     - ✓
     - ✓
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - ✓*
     - ✓
     - ✓
   * - **press_any_key_to_continue**
     - 
     - ✓
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - **print**
     - 
     - 
     - 
     - 
     - 
     - 
     - 
     - ✓
     - 
     - 
     - 
     - 
     - 
     - 
     - 
   * - **form**
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*
     - \*

**Legend:**

- **✓** = Token is used and affects rendering for that prompt
- blank = Token has no effect on that prompt
- **✓\*** = Only when optional feature enabled (see notes)
- **\*** = form: Inherits from child questions
- **search†** = Includes ``search_success``, ``search_none``, ``question-mark`` tokens - only active when ``use_search_filter=True``
- **validation‡** = Includes ``validation-toolbar``, ``bottom-toolbar`` tokens
- **scrollbar.*** = Scrollbar styling for overflowing lists or completion menus
- **completion-menu.*** = Prompt toolkit completion dropdown UI tokens
- **cursor-*** = Includes ``cursor-line`` and ``cursor-column``

Key patterns
************

1. **Simple input prompts** (``text``, ``password``, ``confirm``):
   
   - Use: ``qmark``, ``question``, ``answer``, ``instruction``
   - ``text`` and ``password`` also use ``cursor-*`` during editing
   - These are the "core" tokens

2. **List-based prompts** (``select``, ``rawselect``, ``checkbox``):
   
   - Use core tokens PLUS: ``pointer``, ``highlighted``, ``text``, ``separator``, ``disabled``
   - These add list navigation and choice rendering tokens

3. **Checkbox unique features**:
   
   - Adds ``selected`` (for checked items with ●)
   - Adds ``validation-toolbar``/``bottom-toolbar`` (for error messages)

4. **Autocomplete variations**:
   
   - ``autocomplete``: Uses ``selected`` for dropdown highlighting
   - ``autocomplete`` and ``path`` both use ``completion-menu.*``, ``scrollbar.*``, and ``cursor-*``
   - ``path``: Simple input, no list tokens

5. **Special cases**:
   
   - ``press_any_key_to_continue``: Only uses ``question`` (no prefix, no answer)
   - ``print``: Only uses ``text`` (not a question at all)

**Practical usage:** When styling a prompt, focus on the tokens marked ✓ for that row. Other tokens will be ignored even if you define them.

Prompt Toolkit Style Tokens
############################

Completion Menu Tokens
**********************

These tokens control the appearance of autocomplete dropdown menus (used by ``autocomplete`` and ``path`` prompts):

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Token
     - Default Style
     - Description
   * - ``completion-menu``
     - ``bg:#bbbbbb #000000``
     - The main completion dropdown menu container
   * - ``completion-menu.completion``
     - (empty - inherits from completion-menu)
     - Individual completion item
   * - ``completion-menu.completion.current``
     - ``fg:#888888 bg:#ffffff reverse``
     - Currently highlighted/selected completion item
   * - ``completion-menu.meta.completion``
     - ``bg:#999999 #000000``
     - Meta information (description) for completion items
   * - ``completion-menu.meta.completion.current``
     - ``bg:#aaaaaa #000000``
     - Meta information for currently highlighted item
   * - ``completion-menu.multi-column-meta``
     - ``bg:#aaaaaa #000000``
     - Meta information in multi-column mode
   * - ``completion-menu.completion fuzzymatch.outside``
     - ``fg:#444444``
     - Non-matching text in fuzzy search
   * - ``completion-menu.completion fuzzymatch.inside``
     - ``bold``
     - Matching characters in fuzzy search
   * - ``completion-menu.completion fuzzymatch.inside.character``
     - ``underline``
     - Individual matching characters in fuzzy search
   * - ``completion-menu.completion.current fuzzymatch.outside``
     - ``fg:default``
     - Non-matching text in highlighted item
   * - ``completion-menu.completion.current fuzzymatch.inside``
     - ``nobold``
     - Matching text in highlighted item

Completion Toolbar Tokens
**************************

These tokens style the toolbar that appears above or below the completion menu:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Token
     - Default Style
     - Description
   * - ``completion-toolbar``
     - ``bg:#bbbbbb #000000``
     - Toolbar container
   * - ``completion-toolbar.arrow``
     - ``bg:#bbbbbb #000000 bold``
     - Navigation arrows in toolbar
   * - ``completion-toolbar.completion``
     - ``bg:#bbbbbb #000000``
     - Completion count/status in toolbar
   * - ``completion-toolbar.completion.current``
     - ``bg:#444444 #ffffff``
     - Currently selected item indicator in toolbar

Scrollbar Tokens
****************

These tokens control scrollbar appearance in scrollable regions (completion menus, long choice lists):

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Token
     - Default Style
     - Description
   * - ``scrollbar.background``
     - ``bg:#aaaaaa``
     - Scrollbar track background
   * - ``scrollbar.button``
     - ``bg:#444444``
     - Scrollbar thumb/button
   * - ``scrollbar.arrow``
     - ``noinherit bold``
     - Scrollbar directional arrows
   * - ``scrollbar.start``
     - ``nounderline``
     - Top of scrollbar
   * - ``scrollbar.end``
     - ``nounderline``
     - Bottom of scrollbar

Search and Toolbar Tokens
**************************

These tokens are used for search functionality and various toolbars:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Token
     - Default Style
     - Description
   * - ``search``
     - ``bg:ansibrightyellow ansiblack``
     - Search highlight
   * - ``search.current``
     - (empty - inherits from search)
     - Currently focused search match
   * - ``search-toolbar``
     - ``bold``
     - Search toolbar container
   * - ``search-toolbar.text``
     - ``nobold``
     - Text in search toolbar
   * - ``system-toolbar``
     - ``bold``
     - System message toolbar
   * - ``system-toolbar.text``
     - ``nobold``
     - Text in system toolbar
   * - ``arg-toolbar``
     - ``bold``
     - Argument toolbar (for vi-style commands)
   * - ``arg-toolbar.text``
     - ``nobold``
     - Text in argument toolbar

Other UI Tokens
***************

Additional tokens for various UI elements:

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Token
     - Default Style
     - Description
   * - ``selected``
     - ``reverse``
     - Generic selected text style (used in various contexts)
   * - ``cursor-line``
     - ``underline``
     - Line containing the cursor
   * - ``cursor-column``
     - ``bg:#dddddd``
     - Column containing the cursor
   * - ``matching-bracket``
     - (empty)
     - Matching bracket/parenthesis
   * - ``matching-bracket.other``
     - ``#000000 bg:#aacccc``
     - The other matching bracket
   * - ``matching-bracket.cursor``
     - ``#ff8888 bg:#880000``
     - Matching bracket under cursor
   * - ``line-number``
     - ``#888888``
     - Line numbers (if displayed)
   * - ``line-number.current``
     - ``bold``
     - Current line number
   * - ``auto-suggestion``
     - ``#666666``
     - Auto-suggestion text (ghost text)
   * - ``trailing-whitespace``
     - ``#999999``
     - Trailing whitespace highlighting
   * - ``aborting``
     - ``#888888 bg:default noreverse noitalic nounderline noblink``
     - Style when aborting (Ctrl+C)
   * - ``exiting``
     - ``#888888 bg:default noreverse noitalic nounderline noblink``
     - Style when exiting

Complete Styling Example
########################

Here's a single example that combines basic questionary token styling with more advanced prompt_toolkit UI styling for completion menus, scrollbars, and cursor highlighting:

.. code-block:: python3

   from prompt_toolkit.styles import Style
   import questionary

   CUSTOM_STYLE = Style([
     # Core questionary tokens
     ("qmark", "fg:#673ab7 bold"),
     ("question", "bold"),
     ("answer", "fg:#f44336 bold"),
     ("instruction", "fg:#888888 italic"),

     # List-based prompts
     ("pointer", "fg:#673ab7 bold"),
     ("highlighted", "fg:#673ab7 bold"),
     ("selected", "fg:#cc5454"),
     ("text", "fg:#fbe9e7"),
     ("separator", "fg:#6c6c6c"),
     ("disabled", "fg:#858585 italic"),

     # Search and validation
     ("search_success", "fg:#00ff00 bold"),
     ("search_none", "fg:#ff0000 bold"),
     ("question-mark", "fg:#ff9d00 bold"),
     ("validation-toolbar", "fg:#ffffff bg:#af0000"),

     # Prompt toolkit completion UI
     ("completion-menu", "bg:#1c1c1c fg:#ffffff"),
     ("completion-menu.completion", "bg:#1c1c1c fg:#bbbbbb"),
     ("completion-menu.completion.current", "bg:#005f87 fg:#ffffff bold"),
     ("completion-menu.meta.completion", "bg:#262626 fg:#888888"),
     ("completion-menu.meta.completion.current", "bg:#005f87 fg:#d0d0d0"),
     ("completion-menu.completion fuzzymatch.inside", "fg:#ffaf00 bold"),
     ("completion-menu.completion fuzzymatch.inside.character", "fg:#ffaf00 underline"),

     # Prompt toolkit scrollbars and cursor helpers
     ("scrollbar.background", "bg:#303030"),
     ("scrollbar.button", "bg:#673ab7"),
     ("cursor-line", "underline"),
     ("cursor-column", "bg:#3a3a3a"),
   ])

   name = questionary.text(
     "Your name?",
     instruction="(required)",
     style=CUSTOM_STYLE,
   ).ask()

   language = questionary.autocomplete(
     "Favorite language?",
     choices=["Python", "Rust", "Go", "TypeScript", "Java"],
     style=CUSTOM_STYLE,
   ).ask()

   framework = questionary.select(
     "Pick a framework:",
     choices=["Django", "FastAPI", "Flask"],
     style=CUSTOM_STYLE,
   ).ask()

   extras = questionary.checkbox(
     "Enable extras:",
     choices=["Formatting", "Linting", "Type checking"],
     style=CUSTOM_STYLE,
   ).ask()

This single style object can be reused across simple text prompts, searchable lists, and completion UIs to keep both questionary tokens and prompt_toolkit UI elements visually consistent.
