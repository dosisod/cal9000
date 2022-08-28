import calendar
from datetime import datetime

DAYS_OF_WEEK_HEADER = "Su Mo Tu We Th Fr Sa"


def render_calendar_month_title(date: datetime) -> str:
    title = date.strftime("%B %Y")
    centered = f" {title:^19}"

    return centered


def invert_color(txt: str) -> str:
    return f"\x1b[7m{txt}\x1b[0m"


def render_calendar_cell(day: int, is_selected: bool) -> str:
    display = f"{day or '':>2}"

    return invert_color(display) if is_selected else display


def get_calendar_grid(date: datetime) -> list[list[int]]:
    calendar.setfirstweekday(6)
    return calendar.monthcalendar(date.year, date.month)


def render_calendar(date: datetime) -> str:
    lines = [render_calendar_month_title(date), DAYS_OF_WEEK_HEADER]

    for row in get_calendar_grid(date):
        lines.append(
            " ".join(
                [render_calendar_cell(col, col == date.day) for col in row]
            )
        )

    return "\n".join(lines)
