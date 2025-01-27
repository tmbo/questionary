from typing import Any, Optional
from datetime import datetime

from questionary import Style
from questionary.constants import DEFAULT_QUESTION_PREFIX
from questionary.prompts import text
from questionary.question import Question


def date(
    message: str,
    default: Optional[str] = None,
    validate: Any = None,
    qmark: str = DEFAULT_QUESTION_PREFIX,
    style: Optional[Style] = None,
    format: str = "%Y-%m-%d",
    min_date: Optional[str] = None,
    max_date: Optional[str] = None,
    **kwargs: Any,
) -> Question:
    """
    Prompt the user to enter a date.

    This question type can be used to prompt the user for a date input,
    with optional validation, formatting, and range restrictions.

    Example:
        >>> import questionary
        >>> questionary.date("Enter your birthdate (YYYY-MM-DD):").ask()
        ? Enter your birthdate (YYYY-MM-DD): 1990-01-01
        '1990-01-01'

    Args:
        message: Question text.

        default: Default date value in the given format. Defaults to None.

        validate: Custom validation function for the date input.
                  This can either be a function accepting the input and
                  returning a boolean, or a class reference to a
                  subclass of the prompt toolkit Validator class.

        qmark: Question prefix displayed in front of the question.
               By default this is a ``?``.

        style: A custom color and style for the question parts. You can
               configure colors as well as font types for different elements.

        format: The expected date format (e.g., "%Y-%m-%d"). Defaults to "%Y-%m-%d".

        min_date: The minimum allowed date in the given format. Defaults to None.

        max_date: The maximum allowed date in the given format. Defaults to None.

        kwargs: Additional arguments, they will be passed to prompt toolkit.

    Returns:
        :class:`Question`: Question instance, ready to be prompted (using ``.ask()``).
    """

    def date_validator(input_date: str) -> bool:
        """Validate the entered date based on format and range."""
        try:
            parsed_date = datetime.strptime(input_date, format)

            # Validate minimum date
            if min_date:
                min_date_obj = datetime.strptime(min_date, format)
                if parsed_date < min_date_obj:
                    raise ValueError(
                        f"Date must not be earlier than {min_date}."
                    )

            # Validate maximum date
            if max_date:
                max_date_obj = datetime.strptime(max_date, format)
                if parsed_date > max_date_obj:
                    raise ValueError(
                        f"Date must not be later than {max_date}."
                    )

            return True
        except ValueError as e:
            raise ValueError(str(e))

    # Use the provided validator or the built-in date_validator
    final_validator = validate or date_validator

    return text.text(
        message=message,
        default=default,
        validate=final_validator,
        qmark=qmark,
        style=style,
        **kwargs,
    )


