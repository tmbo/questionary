# -*- coding: utf-8 -*-
"""Example for a autocomplete question type.

Run example by typing `python -m examples.autocomplete` in your console."""
from pprint import pprint

import questionary
from examples import custom_style_fancy

from questionary import Validator, ValidationError, prompt


class PolyergusValidator(Validator):
    def validate(self, document):
        ok = "Polyergus" in document.text
        if not ok:
            raise ValidationError(
                message="Please choose a Polyergus Ant",
                cursor_position=len(document.text),
            )  # Move cursor to end


meta_information = {
    "Camponotus pennsylvanicus": "This is an important, destructive pest that"
    " attacks fences, poles and buildings",
    "Linepithema humile": "It is an invasive species that has been established"
    " in many Mediterranean climate areas",
    "Eciton burchellii": "Known as army ants, moves almost incessantly"
    " over the time it exists",
    "Atta colombica": "They are known for cutting grasses and leaves, carrying"
    " them to their colonies' nests, and growing fungi on"
    " them which they later feed on",
    "Polyergus lucidus": "It is an obligatory social parasite, unable to feed"
    " itself or look after its brood and reliant on ants"
    " of another species of the genus Formica to undertake"
    " these tasks.",
    "Polyergus rufescens": "Is another specie of slave-making ant.",
}


def ask_pystyle(**kwargs):
    # create the question object
    question = questionary.autocomplete(
        "Choose ant specie",
        validate=PolyergusValidator,
        meta_information=meta_information,
        choices=[
            "Camponotus pennsylvanicus",
            "Linepithema humile",
            "Eciton burchellii",
            "Atta colombica",
            "Polyergus lucidus",
            "Polyergus rufescens",
        ],
        ignore_case=False,
        style=custom_style_fancy,
        **kwargs,
    )

    # prompt the user for an answer
    return question.ask()


def ask_dictstyle(**kwargs):
    questions = [
        {
            "type": "autocomplete",
            "name": "ants",
            "choices": [
                "Camponotus pennsylvanicus",
                "Linepithema humile",
                "Eciton burchellii",
                "Atta colombica",
                "Polyergus lucidus",
                "Polyergus rufescens",
            ],
            "meta_information": meta_information,
            "message": "Choose ant specie",
            "validate": PolyergusValidator,
        }
    ]

    return prompt(questions, style=custom_style_fancy, **kwargs)


if __name__ == "__main__":
    pprint(ask_pystyle())
