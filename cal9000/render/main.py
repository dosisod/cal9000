from datetime import datetime, timedelta

from ..config import Keys
from ..ui import View, ui_window
from ..io import Keyboard, Items
from .calendar import render_calendar
from .help import show_help
from .day import items_for_day

# TODO: allow user to change these keybindings
DAY_DIFF = {
    Keys.UP: -7,
    Keys.DOWN: 7,
    Keys.LEFT: -1,
    Keys.RIGHT: 1,
    Keys.DOWN_4: 7 * 4,
    Keys.UP_4: -7 * 4,
}


def main(date: datetime, items: Items, keyboard: Keyboard) -> View:
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
            yield from items_for_day(items, date, keyboard)
