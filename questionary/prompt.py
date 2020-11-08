from prompt_toolkit.output import ColorDepth
from typing import Any, Dict, Optional, Iterable, Mapping

from questionary import utils
from questionary.constants import DEFAULT_KBI_MESSAGE
from questionary.prompts import AVAILABLE_PROMPTS, prompt_by_name


class PromptParameterException(ValueError):
    def __init__(self, message: str, errors: Optional[BaseException] = None) -> None:
        # Call the base class constructor with the parameters it needs
        super().__init__("You must provide a `%s` value" % message, errors)


def prompt(
    questions: Iterable[Mapping[str, Any]],
    answers: Optional[Mapping[str, Any]] = None,
    patch_stdout: bool = False,
    true_color: bool = False,
    kbi_msg: str = DEFAULT_KBI_MESSAGE,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Prompt the user for input on all the questions.

    Catches keyboard interrupts and prints a message."""

    try:
        return unsafe_prompt(questions, answers, patch_stdout, true_color, **kwargs)
    except KeyboardInterrupt:
        print("")
        print(kbi_msg)
        print("")
        return {}


def unsafe_prompt(
    questions: Iterable[Mapping[str, Any]],
    answers: Optional[Mapping[str, Any]] = None,
    patch_stdout: bool = False,
    true_color: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Prompt the user for input on all the questions.

    Won't catch keyboard interrupts.

    Raises:
        KeyboardInterrupt: raised on keyboard interrupt
    """

    if isinstance(questions, dict):
        questions = [questions]

    answers = dict(answers or {})

    for question_config in questions:
        question_config = dict(question_config)
        # import the question
        if "type" not in question_config:
            raise PromptParameterException("type")
        if "name" not in question_config:
            raise PromptParameterException("name")

        choices = question_config.get("choices")
        if choices is not None and callable(choices):
            question_config["choices"] = choices(answers)

        _kwargs = kwargs.copy()
        _kwargs.update(question_config)

        _type = _kwargs.pop("type")
        _filter = _kwargs.pop("filter", None)
        name = _kwargs.pop("name")
        when = _kwargs.pop("when", None)

        if true_color:
            _kwargs["color_depth"] = ColorDepth.TRUE_COLOR

        if when:
            # at least a little sanity check!
            if callable(question_config["when"]):
                try:
                    if not question_config["when"](answers):
                        continue
                except Exception as e:
                    raise ValueError(
                        "Problem in 'when' check of {} " "question: {}".format(name, e)
                    )
            else:
                raise ValueError(
                    "'when' needs to be function that accepts a dict argument"
                )
        if _filter:
            # at least a little sanity check!
            if not callable(_filter):
                raise ValueError(
                    "'filter' needs to be function that accepts an argument"
                )

        if callable(question_config.get("default")):
            _kwargs["default"] = question_config["default"](answers)

        create_question_func = prompt_by_name(_type)

        if not create_question_func:
            raise ValueError(
                "No question type '{}' found. "
                "Known question types are {}."
                "".format(_type, ", ".join(AVAILABLE_PROMPTS))
            )

        missing_args = list(utils.missing_arguments(create_question_func, _kwargs))
        if missing_args:
            raise PromptParameterException(missing_args[0])

        question = create_question_func(**_kwargs)

        answer = question.unsafe_ask(patch_stdout)

        if answer is not None:
            if _filter:
                try:
                    answer = _filter(answer)
                except Exception as e:
                    raise ValueError(
                        "Problem processing 'filter' of {} "
                        "question: {}".format(name, e)
                    )
            answers[name] = answer

    return answers
