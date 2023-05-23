from datetime import datetime

from cal9000.config import Colors

from ..config import Keys
from ..io import DB, Item, Keyboard
from ..ui import View, ui_window


def render_day_date_title(date: datetime) -> str:
    return datetime.strftime(date, "%B %_d, %Y:\n").replace("  ", " ")


def get_items_for_day(db: DB, date: datetime) -> list[str | Item]:
    lines = [str(event) for event in db.events if event.is_on_date(date)]

    return lines + db.items.get(date.strftime("%s"), [])


def render_items_for_day(db: DB, date: datetime, index: int) -> str:
    out = [render_day_date_title(date)]

    items = get_items_for_day(db, date)

    for i, item in enumerate(items):
        if isinstance(item, Item):
            line = f"[{'x' if item.complete else ' '}] {item}"

        else:
            line = f"* {item}"

        out.append(Colors.SELECTED.colorize(line) if i == index else line)

    if not items:
        out.append(f"nothing for today\n\nPress `{Keys.INSERT}` to add item")

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
            if item := prompt_for_new_item():
                db.items[date.strftime("%s")].append(Item(item))

        elif c == Keys.UP:
            if index > 0:
                index -= 1

        elif c == Keys.DOWN:
            if index < len(get_items_for_day(db, date)) - 1:
                index += 1

        elif c in (Keys.COMPLETE, Keys.DELETE):
            daily_items = db.items[date.strftime("%s")]

            if not daily_items:
                continue

            all_items = get_items_for_day(db, date)
            daily_indexes = len(all_items) - len(daily_items)

            if index >= daily_indexes:
                if c == Keys.COMPLETE:
                    daily_items[index - daily_indexes].complete ^= True

                else:
                    daily_items.pop(index - daily_indexes)

                    if (index - daily_indexes) >= len(
                        daily_items
                    ) and index != 0:
                        index -= 1
