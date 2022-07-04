from collections import defaultdict
from datetime import datetime
from unittest.mock import patch
from cal9000.render.calendar import invert_color

from cal9000.render.day import items_for_day, render_items_for_day
from cal9000.config import Keys
from .util import disable_print, keyboard


def test_render_items_for_day_when_there_are_no_items():
    got = render_items_for_day(
        defaultdict(), datetime(month=7, day=1, year=2022), 0
    )

    expected = """\
July 1, 2022:

nothing for today"""

    assert expected == got


def test_render_items_for_day():
    date = datetime(month=7, day=1, year=2022)
    items = {date.strftime("%s"): ["item 1", "item 2"]}

    got = render_items_for_day(defaultdict(list, items), date, 0)

    expected = f"""\
July 1, 2022:

{invert_color('* item 1')}
* item 2"""

    assert expected == got


def test_quit_closes_view():
    with disable_print():
        kb = keyboard([Keys.QUIT])
        states = list(items_for_day(defaultdict(), datetime.now(), kb))

    assert len(states) == 1


def test_any_other_key_just_redraws():
    kb = keyboard(
        [
            "some",
            "key",
            "that",
            "does",
            "nothing",
            Keys.QUIT,
        ]
    )

    with disable_print():
        states = list(items_for_day(defaultdict(), datetime.now(), kb))

    assert len(states) == 6


def test_insert_item_into_day():
    item = "item 1"
    kb = keyboard([Keys.INSERT, Keys.QUIT])

    with disable_print():
        with patch("builtins.input", lambda _: item):
            states = list(items_for_day(defaultdict(list), datetime.now(), kb))

    assert len(states) == 2

    assert item not in states[0]
    assert item in states[1]


def test_move_up_and_down_in_item_list():
    kb = keyboard(
        [Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.UP, Keys.UP, Keys.UP, Keys.QUIT]
    )
    date = datetime.now()
    items = {date.strftime("%s"): ["item 1", "item 2", "item 3"]}

    with disable_print():
        states = list(items_for_day(defaultdict(list, items), date, kb))

    assert len(states) == 7

    assert invert_color("* item 1") in states[0]
    assert invert_color("* item 2") in states[1]
    assert invert_color("* item 3") in states[2]
    assert invert_color("* item 3") in states[3]
    assert invert_color("* item 2") in states[4]
    assert invert_color("* item 1") in states[5]
    assert invert_color("* item 1") in states[6]


def test_delete_item():
    kb = keyboard([Keys.DELETE, Keys.QUIT])
    date = datetime.now()
    items = {date.strftime("%s"): ["item 1"]}

    with disable_print():
        states = list(items_for_day(defaultdict(list, items), date, kb))

    assert len(states) == 2

    assert "* item 1" in states[0]
    assert "* item 1" not in states[1]

    assert len(items[date.strftime("%s")]) == 0
