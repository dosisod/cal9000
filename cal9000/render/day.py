from datetime import datetime

from cal9000.render.calendar import invert_color
from ..io import Items, Keyboard
from ..config import Keys
from ..ui import View, ui_window


def render_day_date_title(date: datetime) -> str:
    return datetime.strftime(date, "%B %_d, %Y:\n").replace("  ", " ")


def render_items_for_day(items: Items, date: datetime, index: int) -> str:
    out = [render_day_date_title(date)]

    lines = items.get(date.strftime("%s"), [])

    for i, line in enumerate(lines):
        bullet_point = f"* {line}"

        out.append(invert_color(bullet_point) if i == index else bullet_point)

    if len(lines) == 0:
        out.append("nothing for today")

    return "\n".join(out)


def prompt_for_new_item() -> str:
    with ui_window(full_reset=True):
        return input("> ")


def items_for_day(items: Items, date: datetime, keyboard: Keyboard) -> View:
    index = 0

    while True:
        with ui_window():
            yield render_items_for_day(items, date, index)

        c = keyboard()

        if c == Keys.QUIT:
            break

        if c == Keys.INSERT:
            item = prompt_for_new_item()
            items[date.strftime("%s")].append(item)

        elif c == Keys.UP:
            if index > 0:
                index -= 1

        elif c == Keys.DOWN:
            if index < len(items.get(date.strftime("%s"), [])) - 1:
                index += 1

        elif c == Keys.DELETE:
            new_items = items[date.strftime("%s")]
            new_items.pop(index)

            if index >= len(new_items) and index != 0:
                index -= 1
