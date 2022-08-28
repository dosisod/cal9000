from datetime import datetime

from cal9000.config import Keys
from cal9000.io import DB
from cal9000.render.calendar import invert_color
from cal9000.render.main import main

from test.render.util import disable_print, keyboard


def test_main_show_help():
    kb = keyboard([Keys.HELP, Keys.QUIT, Keys.QUIT])
    date = datetime.now()

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 3
    assert "help" in states[1]


def test_open_day():
    kb = keyboard([Keys.OPEN, Keys.QUIT, Keys.QUIT])
    date = datetime.now()

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 3
    assert "nothing for today" in states[1]


def test_calendar_go_up_then_home():
    kb = keyboard([Keys.UP, Keys.GO_HOME, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 3
    assert invert_color(" 1") in states[0]
    assert invert_color(" 1") not in states[1]
    assert invert_color(" 1") in states[2]


def test_calendar_go_left():
    kb = keyboard([Keys.LEFT, Keys.QUIT])
    date = datetime(month=7, day=2, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert invert_color(" 2") in states[0]
    assert invert_color(" 1") in states[1]


def test_calendar_go_right():
    kb = keyboard([Keys.RIGHT, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert invert_color(" 1") in states[0]
    assert invert_color(" 2") in states[1]


def test_calendar_go_down():
    kb = keyboard([Keys.DOWN, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert invert_color(" 1") in states[0]
    assert invert_color(" 8") in states[1]


def test_calendar_go_up():
    kb = keyboard([Keys.UP, Keys.QUIT])
    date = datetime(month=7, day=8, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert invert_color(" 8") in states[0]
    assert invert_color(" 1") in states[1]


def test_calendar_go_up_4():
    kb = keyboard([Keys.UP_4, Keys.QUIT])
    date = datetime(month=7, day=29, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert invert_color("29") in states[0]
    assert invert_color(" 1") in states[1]


def test_calendar_go_down_4():
    kb = keyboard([Keys.DOWN_4, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert invert_color(" 1") in states[0]
    assert invert_color("29") in states[1]
