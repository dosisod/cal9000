from datetime import datetime

from cal9000.events import MonthlyEvent, WeeklyEvent
from cal9000.render.calendar import invert_color

from ..config import Keys
from ..io import DB, Keyboard
from ..ui import View, ui_window


def render_day_date_title(date: datetime) -> str:
    return datetime.strftime(date, "%B %_d, %Y:\n").replace("  ", " ")


def get_items_for_day(db: DB, date: datetime) -> list[str]:
    lines = []

    for event in db.events:
        # TODO: move this logic to the event itself
        match event:
            case MonthlyEvent(day=d) if d == date.day:
                lines.append(str(event))

            case WeeklyEvent(weekday=d) if d == (date.isoweekday() % 7):
                lines.append(str(event))

    return lines + db.items.get(date.strftime("%s"), [])


def render_items_for_day(db: DB, date: datetime, index: int) -> str:
    out = [render_day_date_title(date)]

    items = get_items_for_day(db, date)

    for i, line in enumerate(items):
        bullet_point = f"* {line}"

        out.append(invert_color(bullet_point) if i == index else bullet_point)

    if len(items) == 0:
        out.append("nothing for today")

    return "\n".join(out)


def prompt_for_new_item() -> str:
    with ui_window(full_reset=True):
        return input("> ")


def items_for_day(db: DB, date: datetime, keyboard: Keyboard) -> View:
    index = 0

    while True:
        with ui_window():
            yield render_items_for_day(db, date, index)

        c = keyboard()

        if c == Keys.QUIT:
            break

        if c == Keys.INSERT:
            item = prompt_for_new_item()
            db.items[date.strftime("%s")].append(item)

        elif c == Keys.UP:
            if index > 0:
                index -= 1

        elif c == Keys.DOWN:
            if index < len(get_items_for_day(db, date)) - 1:
                index += 1

        elif c == Keys.DELETE:
            daily_items = db.items[date.strftime("%s")]

            if len(daily_items) == 0:
                continue

            all_items = get_items_for_day(db, date)
            deleteable_indexes = len(all_items) - len(daily_items)

            if index >= deleteable_indexes:
                daily_items.pop(index - deleteable_indexes)

                if (index - deleteable_indexes) >= len(
                    daily_items
                ) and index != 0:
                    index -= 1
