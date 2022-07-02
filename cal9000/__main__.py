import sys

from cal9000.date import get_today_date_only
from cal9000.io import load_save_file, save_items
from cal9000.render.main import main
from cal9000.ui import root_window


items = load_save_file()
keyboard = lambda: sys.stdin.read(1)
date = get_today_date_only()

with root_window():
    for draw in main(date, items, keyboard):
        print(draw, end="")

save_items(items)
