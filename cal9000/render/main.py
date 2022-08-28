from datetime import datetime, timedelta

from ..config import Keys
from ..io import DB, Keyboard
from ..ui import View, ui_window
from .calendar import render_calendar
from .day import items_for_day
from .event_manager import recurring_event_manager
from .help import show_help

# TODO: allow user to change these keybindings
DAY_DIFF = {
    Keys.UP: -7,
    Keys.DOWN: 7,
    Keys.LEFT: -1,
    Keys.RIGHT: 1,
    Keys.DOWN_4: 7 * 4,
    Keys.UP_4: -7 * 4,
}


def main(date: datetime, db: DB, keyboard: Keyboard) -> View:
    start_date = date

    while True:
        with ui_window():
            yield render_calendar(date)

        c = keyboard()

        if c == Keys.QUIT:
            break

        if days := DAY_DIFF.get(c):
            date += timedelta(days=days)

        elif c == Keys.GO_HOME:
            date = start_date

        elif c == Keys.HELP:
            yield from show_help(keyboard)

        elif c == Keys.OPEN:
            yield from items_for_day(db, date, keyboard)

        elif c == Keys.GOTO_EVENTS:
            yield from recurring_event_manager(db, keyboard)
