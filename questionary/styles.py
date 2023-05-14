from typing import List
from typing import Optional

import prompt_toolkit.styles

from questionary.constants import DEFAULT_STYLE


def merge_styles_default(styles: List[Optional[prompt_toolkit.styles.Style]]):
    filtered_styles: list[prompt_toolkit.styles.BaseStyle] = [DEFAULT_STYLE]
    filtered_styles.extend([s for s in styles if s is not None])
    return prompt_toolkit.styles.merge_styles(filtered_styles)
