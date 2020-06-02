import re


def improve_text(text):
    text = re.sub(r"(\s)-(\s)", "\u00A0—\\2", text)
    text = add_nbsp(text)
    text = add_nbsp(text)
    text = add_nbsp(text)

    return text


def add_nbsp(text):
    return re.sub(
        r"(\s(и|а|в|не|на|для|о|об|у|к|с|со|за|по)) ([a-zа-яё0-9])",
        "\\1\u00A0\\3",
        text,
        flags=re.IGNORECASE,
    )


def cut(text, length):
    if len(text) <= length:
        return text

    i = max(0, length - 4)
    while i > 0 and text[i] != " ":
        i -= 1

    if i == 0:
        return f"{text[:length - 3]}..."

    return f"{text[:i]} ..."
