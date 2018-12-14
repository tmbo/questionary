import prompt_toolkit.patch_stdout

from questionary.constants import DEFAULT_KBI_MESSAGE


class Question:
    """A question to be prompted.

    This is an internal class. Questions should be created using the
    predefined questions (e.g. text or password)."""

    def __init__(self, application):
        self.application = application

    def ask(self, patch_stdout=False, kbi_msg=DEFAULT_KBI_MESSAGE):
        try:
            return self.unsafe_ask(patch_stdout)
        except KeyboardInterrupt:
            print("\n{}\n".format(kbi_msg))
            return None

    def unsafe_ask(self, patch_stdout=False):
        if patch_stdout:
            with prompt_toolkit.patch_stdout.patch_stdout():
                return self.application.run()
        else:
            return self.application.run()
