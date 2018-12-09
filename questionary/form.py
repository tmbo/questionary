from collections import namedtuple

from questionary.constants import DEFAULT_KBI_MESSAGE
from questionary.question import Question

FormField = namedtuple("FormField", ["key", "question"])


def form(**kwargs: Question):
    return Form(*(FormField(k, q) for k, q in kwargs.items()))


class Form:
    def __init__(self, *form_fields: FormField):
        self.form_fields = form_fields

    def unsafe_ask(self, patch_stdout=False):
        answers = {}
        for f in self.form_fields:
            answers[f.key] = f.question.unsafe_ask(patch_stdout)
        return answers

    def ask(self, patch_stdout=False, kbi_msg=DEFAULT_KBI_MESSAGE):
        try:
            return self.unsafe_ask(patch_stdout)
        except KeyboardInterrupt:
            print('')
            print(kbi_msg)
            print('')
            return {}
