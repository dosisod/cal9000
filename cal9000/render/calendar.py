import calendar
from datetime import datetime

from cal9000.config import Colors
from cal9000.events import MonthlyEvent, WeeklyEvent
from cal9000.io import DB

DAYS_OF_WEEK_HEADER = "Su Mo Tu We Th Fr Sa"


def render_calendar_month_title(date: datetime) -> str:
    title = date.strftime("%B %Y")
    centered = f" {title:^19}"

    return centered


def render_calendar_cell(day: int, color: Colors | None = None) -> str:
    display = f"{day or '':>2}"

    return color.colorize(display) if color else display


def get_calendar_grid(date: datetime) -> list[list[int]]:
    calendar.setfirstweekday(6)
    return calendar.monthcalendar(date.year, date.month)


def render_calendar(date: datetime, db: DB) -> str:
    lines = [render_calendar_month_title(date), DAYS_OF_WEEK_HEADER]

    weekdays = set[int]()
    days = set[int]()

    for event in db.events:
        match event:
            case WeeklyEvent(weekday=day):
                weekdays.add(day)

            case MonthlyEvent(day=day):
                days.add(day)

    for week in get_calendar_grid(date):
        cells = []

        for day in week:
            color = None

            if day == date.day:
                color = Colors.SELECTED

            elif day:
                cell_date = date.replace(day=day)

                if (
                    cell_date.day in days
                    or (cell_date.isoweekday() % 7) in weekdays
                    or db.items.get(cell_date.strftime("%s"))
                ):
                    color = Colors.HAS_ITEM

            cells.append(render_calendar_cell(day, color))

        lines.append(" ".join(cells))

    return "\n".join(lines)
