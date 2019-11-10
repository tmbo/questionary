from prompt_toolkit.styles import Style

custom_style_fancy = Style(
    [
        ("separator", "fg:#cc5454"),
        ("qmark", "fg:#673ab7 bold"),
        ("question", ""),
        ("selected", "fg:#cc5454"),
        ("pointer", "fg:#673ab7 bold"),
        ("highlighted", "fg:#673ab7 bold"),
        ("answer", "fg:#f44336 bold"),
        ("text", "fg:#FBE9E7"),
        ("disabled", "fg:#858585 italic"),
    ]
)

custom_style_dope = Style(
    [
        ("separator", "fg:#6C6C6C"),
        ("qmark", "fg:#FF9D00 bold"),
        ("question", ""),
        ("selected", "fg:#5F819D"),
        ("pointer", "fg:#FF9D00 bold"),
        ("answer", "fg:#5F819D bold"),
    ]
)

custom_style_genius = Style(
    [
        ("qmark", "fg:#E91E63 bold"),
        ("question", ""),
        ("selected", "fg:#673AB7 bold"),
        ("answer", "fg:#2196f3 bold"),
    ]
)
