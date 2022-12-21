from calendar import monthrange
from datetime import datetime, timedelta

from ..command_bar import CommandBar
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
    cmd_bar = CommandBar(20)

    while True:
        with ui_window():
            calendar = render_calendar(date, db)

            if bar := str(cmd_bar):
                calendar = f"{calendar}\n{bar}"

            yield calendar

        c = keyboard()

        if c == "\n":
            if cmd_bar.command in (":help", ":h"):
                yield from show_help(keyboard)

            elif cmd_bar.command in (":quit", ":q"):
                break

            elif (day := cmd_bar.command[1:]).isdigit():
                max_day = monthrange(date.year, date.month)[1]

                date = date.replace(day=max(1, min(int(day), max_day)))

        elif cmd_bar.append(c):
            continue

        if c == Keys.QUIT:
            break

        if days := DAY_DIFF.get(c):
            date += timedelta(days=days) * (cmd_bar.count or 1)

        elif c == Keys.GO_HOME:
            date = start_date

        elif c == Keys.HELP:
            yield from show_help(keyboard)

        elif c == Keys.OPEN:
            yield from items_for_day(db, date, keyboard)

        elif c == Keys.GOTO_EVENTS:
            yield from recurring_event_manager(db, keyboard)

        cmd_bar.reset()
