from datetime import datetime
from unittest.mock import patch

from cal9000.config import Keys
from cal9000.events import MonthlyEvent, WeeklyEvent
from cal9000.io import DB, Items
from cal9000.render.calendar import invert_color
from cal9000.render.day import items_for_day, render_items_for_day

from .util import disable_print, keyboard


def test_render_items_for_day_when_there_are_no_items() -> None:
    got = render_items_for_day(DB(), datetime(month=7, day=1, year=2022), 0)

    expected = """\
July 1, 2022:

nothing for today"""

    assert expected == got


def test_render_items_for_day() -> None:
    date = datetime(month=7, day=1, year=2022)
    items = {date.strftime("%s"): ["item 1", "item 2"]}

    got = render_items_for_day(DB(items=Items(list, items)), date, 0)

    expected = f"""\
July 1, 2022:

{invert_color('* item 1')}
* item 2"""

    assert expected == got


def test_quit_closes_view() -> None:
    with disable_print():
        kb = keyboard([Keys.QUIT])
        states = list(items_for_day(DB(), datetime.now(), kb))

    assert len(states) == 1


def test_any_other_key_just_redraws() -> None:
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
        states = list(items_for_day(DB(), datetime.now(), kb))

    assert len(states) == 6


def test_insert_item_into_day() -> None:
    item = "item 1"
    kb = keyboard([Keys.INSERT, Keys.QUIT])

    with disable_print():
        with patch("builtins.input", lambda _: item):
            db = DB(items=Items(list))
            states = list(items_for_day(db, datetime.now(), kb))

    assert len(states) == 2

    assert item not in states[0]
    assert item in states[1]


def test_move_up_and_down_in_item_list() -> None:
    kb = keyboard(
        [Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.UP, Keys.UP, Keys.UP, Keys.QUIT]
    )
    date = datetime.now()
    items = {date.strftime("%s"): ["item 1", "item 2", "item 3"]}

    with disable_print():
        db = DB(items=Items(list, items))
        states = list(items_for_day(db, date, kb))

    assert len(states) == 7

    assert invert_color("* item 1") in states[0]
    assert invert_color("* item 2") in states[1]
    assert invert_color("* item 3") in states[2]
    assert invert_color("* item 3") in states[3]
    assert invert_color("* item 2") in states[4]
    assert invert_color("* item 1") in states[5]
    assert invert_color("* item 1") in states[6]


def test_delete_item() -> None:
    kb = keyboard([Keys.DELETE, Keys.QUIT])
    date = datetime.now()
    items = {date.strftime("%s"): ["item 1"]}

    with disable_print():
        db = DB(items=Items(list, items))
        states = list(items_for_day(db, date, kb))

    assert len(states) == 2

    assert "* item 1" in states[0]
    assert "* item 1" not in states[1]

    assert len(items[date.strftime("%s")]) == 0


def test_delete_item_when_there_are_no_more_items_does_nothing() -> None:
    kb = keyboard([Keys.DELETE, Keys.QUIT])
    date = datetime.now()
    items: dict[str, list[str]] = {date.strftime("%s"): []}

    with disable_print():
        states = list(items_for_day(DB(items=Items(list, items)), date, kb))

    assert len(states) == 2
    assert items[date.strftime("%s")] == []


def test_delete_last_item_moves_to_next_item() -> None:
    kb = keyboard([Keys.DOWN, Keys.DELETE, Keys.QUIT])
    date = datetime.now()
    items: dict[str, list[str]] = {date.strftime("%s"): ["x", "y"]}

    with disable_print():
        states = list(items_for_day(DB(items=Items(list, items)), date, kb))

    assert len(states) == 3
    assert items[date.strftime("%s")] == ["x"]


def test_items_are_added_if_monthly_event_lands_on_today() -> None:
    event = MonthlyEvent(title="some_title", day=1)
    db = DB(events=[event])

    render = render_items_for_day(db, datetime(month=7, day=1, year=2022), 0)

    assert str(event) in render


def test_items_are_added_if_weekly_event_lands_on_today() -> None:
    event = WeeklyEvent(title="some_title", weekday=0)
    db = DB(events=[event])

    # a day that happens to be a sunday
    sunday = datetime(month=9, day=4, year=2022)

    render = render_items_for_day(db, sunday, 0)

    assert str(event) in render


def test_no_items_added_if_no_events_match_today() -> None:
    monthly_event = MonthlyEvent(title="some_title", day=1)
    weekly_event = WeeklyEvent(title="some_title", weekday=0)
    db = DB(events=[weekly_event, monthly_event])

    render = render_items_for_day(db, datetime(month=9, day=8, year=2022), 0)

    assert str(monthly_event) not in render
    assert str(weekly_event) not in render
