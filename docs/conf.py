import json
import os
import sys
import traceback

sys.path.insert(0, os.path.abspath("../"))
from questionary import __version__

project = "Questionary"
copyright = "2020, Questionary"
author = "Questionary"

version = __version__
release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_autodoc_typehints",
]

nitpick_ignore = [
    ("py:class", "questionary.prompts.common.Choice"),
    ("py:class", "questionary.question.Question"),
    ("py:class", "questionary.form.Form"),
]

autodoc_typehints = "description"

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "navigation_depth": 2,
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "prompt_toolkit": ("https://python-prompt-toolkit.readthedocs.io/en/master/", None),
}

autodoc_member_order = "alphabetical"

# TODO: remove as soon as we upgrade to sphinx 4.0
# Borrowed from https://github.com/sphinx-doc/sphinx/issues/5603
intersphinx_aliases = {
    ("py:class", "prompt_toolkit.styles.style.Style"): (
        "py:class",
        "prompt_toolkit.styles.Style",
    ),
    ("py:class", "prompt_toolkit.shortcuts.prompt.CompleteStyle"): (
        "py:class",
        "prompt_toolkit.shortcuts.CompleteStyle",
    ),
    ("py:class", "prompt_toolkit.completion.base.Completer"): (
        "py:class",
        "prompt_toolkit.completion.Completer",
    ),
    ("py:class", "prompt_toolkit.lexers.base.Lexer"): (
        "py:class",
        "prompt_toolkit.lexers.Lexer",
    ),
}


def add_intersphinx_aliases_to_inv(app):
    from sphinx.ext.intersphinx import InventoryAdapter

    inventories = InventoryAdapter(app.builder.env)

    for alias, target in app.config.intersphinx_aliases.items():
        alias_domain, alias_name = alias
        target_domain, target_name = target

        try:
            found = inventories.main_inventory[target_domain][target_name]
            inventories.main_inventory[alias_domain][alias_name] = found
        except KeyError as e:
            traceback.print_exc()
            continue


def setup(app):
    app.add_config_value("intersphinx_aliases", {}, "env")
    app.connect("builder-inited", add_intersphinx_aliases_to_inv)
