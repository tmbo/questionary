import pytest
from prompt_toolkit.input.defaults import create_pipe_input
from prompt_toolkit.output import DummyOutput
from questionary.prompts.date import date


def test_date_prompt_with_default():
    """Test de saisie avec une valeur par défaut."""
    with create_pipe_input() as pipe_input:
        pipe_input.send_text("\n")  # L'utilisateur appuie simplement sur Entrée
        result = date(
            "Enter a date (default is 2023-01-01):",
            default="2023-01-01",  # Définit une valeur par défaut valide
            input=pipe_input,
            output=DummyOutput()
        ).ask()
        assert result == "2023-01-01"