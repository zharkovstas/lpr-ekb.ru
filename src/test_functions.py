from typing import Tuple

import pytest

from tools.texts import add_nbsp


@pytest.mark.parametrize(
    ("text", "replace_indexes"),
    [(" для партии", (4,)), (" для для для для", (4, 12)), (" по", ()),],
)
def test_add_nbsp(text: str, replace_indexes: Tuple[int]):
    actual = add_nbsp(text)

    if replace_indexes is not None:
        for replace_index in replace_indexes:
            assert ord(text[replace_index]) == 32  # space
            assert ord(actual[replace_index]) == 160  # \u00A0 (&nbsp;)
