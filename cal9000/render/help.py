from ..ui import View, ui_window
from ..io import Keyboard


def show_help(keyboard: Keyboard) -> View:
    with ui_window():
        yield """\
General help:

q\tquit
h\tprevious day
l\tnext day
j\tdown 1 row
J\tdown 4 rows
k\tup 1 row
K\tup 4 rows
u\tgo to current day
o\topen selected day
?\topen this menu
i\tinsert item
"""

    keyboard()
