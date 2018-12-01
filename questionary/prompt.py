# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from prompt_toolkit.output import ColorDepth

from questionary import prompts, utils
import prompt_toolkit.patch_stdout


class PromptParameterException(ValueError):
    def __init__(self, message, errors=None):
        # Call the base class constructor with the parameters it needs
        super(PromptParameterException, self).__init__(
            'You must provide a `%s` value' % message, errors)


def prompt(questions,
           answers=None,
           patch_stdout=False,
           true_color=False,
           kbi_msg='Cancelled by user',
           **kwargs):
    if isinstance(questions, dict):
        questions = [questions]

    answers = answers or {}

    for question in questions:
        # import the question
        if 'type' not in question:
            raise PromptParameterException('type')
        if 'name' not in question:
            raise PromptParameterException('name')
        if 'message' not in question:
            raise PromptParameterException('message')

        choices = question.get('choices')
        if choices is not None and callable(choices):
            question['choices'] = choices(answers)

        _kwargs = {}
        _kwargs.update(kwargs)
        _kwargs.update(question)
        _type = _kwargs.pop('type')
        name = _kwargs.pop('name')
        when = _kwargs.pop('when', None)
        _filter = _kwargs.pop('filter', None)

        if true_color:
            _kwargs["color_depth"] = ColorDepth.TRUE_COLOR

        try:
            if when:
                # at least a little sanity check!
                if callable(question['when']):
                    try:
                        if not question['when'](answers):
                            continue
                    except Exception as e:
                        raise ValueError("Problem in 'when' check of {} "
                                         "question: {}".format(name, e))
                else:
                    raise ValueError("'when' needs to be function that "
                                     "accepts a dict argument")
            if _filter:
                # at least a little sanity check!
                if not callable(_filter):
                    raise ValueError("'filter' needs to be function that "
                                     "accepts an argument")

            if callable(question.get('default')):
                _kwargs['default'] = question['default'](answers)

            question_f = getattr(prompts, _type).question

            missing_args = list(utils.missing_arguments(question_f, _kwargs))
            if missing_args:
                raise PromptParameterException(missing_args[0])

            application = question_f(**_kwargs)

            if patch_stdout:
                with prompt_toolkit.patch_stdout.patch_stdout():
                    answer = application.run()
            else:
                answer = application.run()

            if answer is not None:
                if _filter:
                    try:
                        answer = _filter(answer)
                    except Exception as e:
                        raise ValueError("Problem processing 'filter' of {} "
                                         "question: {}".format(name, e))
                answers[name] = answer
        except AttributeError as e:
            print(e)
            raise ValueError("No question type '{}'".format(_type))
        except KeyboardInterrupt:
            print('')
            print(kbi_msg)
            print('')
            return {}
    return answers

# TODO:
# Bottom Bar - inquirer.ui.BottomBar
