from cal9000.config import Keys
from cal9000.dates import WEEK_DAY_NAMES
from cal9000.events import Event, MonthlyEvent, WeeklyEvent
from cal9000.io import DB, Keyboard
from cal9000.ui import View, ui_window


def interval_to_int(s: str) -> int:
    return int(s[:-2] if s.endswith(("st", "nd", "rd", "th")) else s)


def render_events(events: list[Event]) -> str:
    if len(events) == 0:
        formatted = "No recurring events"

    else:
        formatted = "\n".join(f"* {event}" for event in events)

    return f"Recurring events:\n\n{formatted}"


EVENT_HELP_MSG = """
Events are entered in one of the following forms:

Monthly events:

* N(th) of [every | the] month

Weekly events:

* every WEEKDAY
* WEEKDAY
"""


def parse_event(description: str, event: str) -> Event | None:
    match event.lower().split():
        # TODO: move logic to the event itself
        case [interval, "of", "every" | "the", "month"]:
            return MonthlyEvent(description, interval_to_int(interval))

        case ["every", day] | [day]:
            try:
                weekday = WEEK_DAY_NAMES.index(day.lower())

                return WeeklyEvent(description, weekday)
            except ValueError:
                pass

    return None


def recurring_event_manager(db: DB, keyboard: Keyboard) -> View:
    while True:
        with ui_window():
            yield render_events(db.events)

        c = keyboard()

        if c == Keys.QUIT:
            break

        if c == Keys.INSERT:
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
