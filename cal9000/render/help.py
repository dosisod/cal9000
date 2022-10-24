from ..config import Keys
from ..io import Keyboard
from ..ui import View, ui_window


def help_message() -> str:
    return f"""\
General help:

{Keys.QUIT}\tquit
{Keys.LEFT}\tprevious day
{Keys.RIGHT}\tnext day
{Keys.DOWN}\tdown 1 row
{Keys.DOWN_4}\tdown 4 rows
{Keys.UP}\tup 1 row
{Keys.UP_4}\tup 4 rows
{Keys.GO_HOME}\tgo to current day
{Keys.OPEN}\topen selected day
{Keys.HELP}\topen this menu
{Keys.INSERT}\tinsert item
{Keys.GOTO_EVENTS}\tgoto recurring event manager
"""


def show_help(keyboard: Keyboard) -> View:
    with ui_window():
        yield help_message()

    keyboard()
