import questionary
from examples import custom_style_dope

zoo_animals = [
    "Lion",
    "Tiger",
    "Elephant",
    "Giraffe",
    "Zebra",
    "Panda",
    "Kangaroo",
    "Gorilla",
    "Chimpanzee",
    "Orangutan",
    "Hippopotamus",
    "Rhinoceros",
    "Leopard",
    "Cheetah",
    "Polar Bear",
    "Grizzly Bear",
    "Penguin",
    "Flamingo",
    "Peacock",
    "Ostrich",
    "Emu",
    "Koala",
    "Sloth",
    "Armadillo",
    "Meerkat",
    "Lemur",
    "Red Panda",
    "Wolf",
    "Fox",
    "Otter",
    "Sea Lion",
    "Walrus",
    "Seal",
    "Crocodile",
    "Alligator",
    "Python",
    "Boa Constrictor",
    "Iguana",
    "Komodo Dragon",
    "Tortoise",
    "Turtle",
    "Parrot",
    "Toucan",
    "Macaw",
    "Hyena",
    "Jaguar",
    "Anteater",
    "Capybara",
    "Bison",
    "Moose",
]


if __name__ == "__main__":
    toppings = (
        questionary.checkbox(
            "Select animals for your zoo",
            choices=zoo_animals,
            validate=lambda a: (
                True if len(a) > 0 else "You must select at least one zoo animal"
            ),
            style=custom_style_dope,
            use_jk_keys=False,
            use_search_filter=True,
        ).ask()
        or []
    )

    print(
        f"Alright let's create our zoo with following animals: {', '.join(toppings)}."
    )
