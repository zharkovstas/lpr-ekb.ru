import datetime


months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


def format_date(date):
    result = [str(date.day), months[date.month - 1]]
    if datetime.date.today().year > date.year:
        result.append(str(date.year))

    return " ".join(result)
