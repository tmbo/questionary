from typing import Any, Dict, Iterable, Mapping, Optional, Union
from prompt_toolkit.output import ColorDepth
from questionary import utils, prompts, constants

class PromptParameterException(ValueError):
    """Received a prompt with a missing parameter."""

    def __init__(self, message: str, errors: Optional[BaseException] = None) -> None:
        super().__init__(f"You must provide a `{message}` value", errors)


def prompt(
    questions: Union[Dict[str, Any], Iterable[Mapping[str, Any]]],
    answers: Optional[Mapping[str, Any]] = None,
    patch_stdout: bool = False,
    true_color: bool = False,
    kbi_msg: str = constants.DEFAULT_KBI_MESSAGE,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Prompt the user for input on all the questions, with exception handling."""

    try:
        return unsafe_prompt(questions, answers, patch_stdout, true_color, **kwargs)
    except KeyboardInterrupt:
        print(kbi_msg)
        return {}


def unsafe_prompt(
    questions: Union[Dict[str, Any], Iterable[Mapping[str, Any]]],
    answers: Optional[Mapping[str, Any]] = None,
    patch_stdout: bool = False,
    true_color: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Prompt the user for input on all the questions without interrupt handling."""

    if isinstance(questions, dict):
        questions = [questions]

    answers = dict(answers or {})

    for question_config in questions:
        question_config = dict(question_config)

        if "type" not in question_config:
            raise PromptParameterException("type")
        if "name" not in question_config and question_config["type"] != "print":
            raise PromptParameterException("name")

        _kwargs = kwargs.copy()
        _kwargs.update(question_config)

        _type = _kwargs.pop("type")
        _filter = _kwargs.pop("filter", None)
        name = _kwargs.pop("name", None) if _type == "print" else _kwargs.pop("name")
        when = _kwargs.pop("when", None)

        if true_color:
            _kwargs["color_depth"] = ColorDepth.TRUE_COLOR

        if callable(when) and not when(answers):
            continue

        if _type == "print":
            message = _kwargs.pop("message", None)
            if not message:
                raise PromptParameterException("message")

            _kwargs.pop("input", None)
            prompts.common.print_formatted_text(message, **_kwargs)
            if name:
                answers[name] = None
            continue

        choices = question_config.get("choices")
        if callable(choices):
            calculated_choices = choices(answers)
            question_config["choices"] = calculated_choices
            kwargs["choices"] = calculated_choices

        if callable(question_config.get("default")):
            _kwargs["default"] = question_config["default"](answers)

        create_question_func = prompts.prompt_by_name(_type)

        if not create_question_func:
            raise ValueError(
                f"No question type '{_type}' found. "
                f"Known question types are {', '.join(prompts.AVAILABLE_PROMPTS)}."
            )

        missing_args = list(utils.missing_arguments(create_question_func, _kwargs))
        if missing_args:
            raise PromptParameterException(missing_args[0])

        question = create_question_func(**_kwargs)
        answer = question.unsafe_ask(patch_stdout)

        if answer is not None and _filter:
            try:
                answer = _filter(answer)
            except Exception as exception:
                raise ValueError(
                    f"Problem processing 'filter' of {name} "
                    f"question: {exception}"
                ) from exception
        answers[name] = answer

    return answers
