from datetime import datetime
from ..io import Items, Keyboard
from ..config import Keys
from ..ui import View, ui_window


def render_items_for_day(items: Items, date: datetime) -> str:
    out = datetime.strftime(date, "%B %_d, %Y:\n\n").replace("  ", " ")

    lines = items.get(date.strftime("%s"), [])

    for line in lines:
        out += f"* {line}\n"

    if len(lines) == 0:
        out += "nothing for today\n"

    return out


def prompt_for_new_item() -> str:
    with ui_window(full_reset=True):
        return input("> ")


def items_for_day(items: Items, date: datetime, keyboard: Keyboard) -> View:
    while True:
        with ui_window():
            yield render_items_for_day(items, date)

        c = keyboard()

        if c == Keys.QUIT:
            break

        if c == Keys.INSERT:
            item = prompt_for_new_item()
            items[date.strftime("%s")].append(item)
