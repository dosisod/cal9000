import calendar
from contextlib import suppress

from cal9000.config import Colors, Keys
from cal9000.dates import WEEK_DAY_NAMES
from cal9000.events import Event, MonthlyEvent, WeeklyEvent, YearlyEvent
from cal9000.io import DB, Keyboard
from cal9000.ui import View, ui_window


def interval_to_int(s: str) -> int:
    return int(s[:-2] if s.endswith(("st", "nd", "rd", "th")) else s)


def render_events(events: list[Event], index: int = 0) -> str:
    if len(events) == 0:
        formatted = f"No recurring events\n\nPress `{Keys.INSERT}` to add event"  # noqa: E501

    else:
        lines: list[str] = []

        for i, event in enumerate(events):
            line = f"* {event}"

            if i == index:
                line = Colors.SELECTED.colorize(line)

            lines.append(line)

        formatted = "\n".join(lines)

    return f"Recurring events:\n\n{formatted}"


EVENT_HELP_MSG = """
Events are entered in one of the following forms:

Monthly events:

* N(th) of [every | the] month

Weekly events:

* every WEEKDAY
* WEEKDAY

Yearly events:

* MONTH DAY
"""


def parse_event(description: str, event: str) -> Event | None:
    match event.lower().split():
        # TODO: move logic to the event itself
        case [interval, "of", "every" | "the", "month"]:
            return MonthlyEvent(description, interval_to_int(interval))

        case ["every", day] | [day]:
            with suppress(ValueError):
                weekday = WEEK_DAY_NAMES.index(day.lower())

                return WeeklyEvent(description, weekday)

        case [month_name, day]:
            with suppress(ValueError):
                return YearlyEvent(
                    description,
                    [m.lower() for m in calendar.month_name].index(month_name),
                    interval_to_int(day),
                )

    return None


def recurring_event_manager(db: DB, keyboard: Keyboard) -> View:
    event_index = 0

    while True:
        with ui_window():
            yield render_events(db.events, event_index)

        c = keyboard()

        if c == Keys.QUIT:
            break

        elif c == Keys.INSERT:
            with ui_window(full_reset=True):
                print("Event description")
                description = input("> ")

                if not description:
                    continue

                print(EVENT_HELP_MSG)

                while True:
                    format = input("> ")
                    if not format:
                        break

                    if event := parse_event(description, format):
                        db.events.append(event)
                        break

        elif c == Keys.UP:
            event_index -= 1

        elif c == Keys.DOWN:
            event_index += 1

        elif c == Keys.DELETE:
            db.events.pop(event_index)

        if event_index == len(db.events):
            event_index -= 1

        if event_index < 0:
            event_index = 0
