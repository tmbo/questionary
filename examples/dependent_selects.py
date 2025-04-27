from pprint import pprint

from questionary import prompt

OPTIONS = {"key1": ["k1v1", "k1v2"], "key2": ["k2v1", "k2v2"]}


def ask_dictstyle(**kwargs):
    questions = [
        {
            "type": "select",
            "name": "key",
            "message": "Choose a key",
            "choices": OPTIONS.keys(),
        },
        {
            "type": "select",
            "name": "value",
            "message": "Choose a value",
            "choices": lambda x: OPTIONS[x["key"]],
        },
    ]
    return prompt(questions, **kwargs)


if __name__ == "__main__":
    pprint(ask_dictstyle())
