import sys

from cal9000.date import get_today_date_only
from cal9000.io import load_save_file, save_items
from cal9000.render.main import main as ui_main
from cal9000.ui import (
    clear_screen,
    cursor_set_pos,
    root_window,
    save_cursor_pos,
)


def main() -> None:
    db = load_save_file()
    date = get_today_date_only()

    def keyboard() -> str:
        if (c := sys.stdin.read(1)) != "\x0C":
            return c

        clear_screen()
        cursor_set_pos()
        save_cursor_pos()

        return "\x00"

    with root_window():
        for draw in ui_main(date, db, keyboard):
            print(draw, end="")

    save_items(db)


if __name__ == "__main__":
    main()
