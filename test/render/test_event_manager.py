from unittest.mock import patch

from cal9000.config import Colors, Keys
from cal9000.events import MonthlyEvent, WeeklyEvent, YearlyEvent
from cal9000.io import DB
from cal9000.render.event_manager import recurring_event_manager, render_events

from .util import disable_print, keyboard


def test_render_events() -> None:
    event = MonthlyEvent(title="some title", day=1)
    got = render_events([event])

    line = Colors.SELECTED.colorize(f"* {event}")

    expected = f"""\
Recurring events:

{line}"""

    assert got == expected


def test_render_events_with_no_events() -> None:
    got = render_events([])

    expected = """\
Recurring events:

No recurring events

Press `i` to add event"""

    assert got == expected


def test_quit() -> None:
    with disable_print():
        kb = keyboard([Keys.QUIT])
        states = list(recurring_event_manager(DB(), kb))

    assert len(states) == 1


def test_insert_monthly_event() -> None:
    db = DB()

    with disable_print():
        with patch("builtins.input") as p:
            p.side_effect = ["comment", "1st of every month"]

            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2
    assert "comment" in states[1]

    assert db.events == [MonthlyEvent("comment", day=1)]


def test_insert_weekly_event() -> None:
    db = DB()

    with disable_print():
        with patch("builtins.input") as p:
            p.side_effect = ["comment", "every sunday"]

            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2
    assert "comment" in states[1]

    assert db.events == [WeeklyEvent("comment", weekday=0)]


def test_insert_yearly_event() -> None:
    db = DB()

    with disable_print():
        with patch("builtins.input") as p:
            p.side_effect = ["comment", "January 1st"]

            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2
    assert "comment" in states[1]

    assert db.events == [YearlyEvent("comment", month=1, day=1)]


def test_typing_invalid_event_will_ask_you_again() -> None:
    db = DB()

    with disable_print():
        with patch("builtins.input") as p:
            p.side_effect = [
                "comment",
                "every invalid_weekday",
                "every monday",
            ]

            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2
    assert "comment" in states[1]

    assert db.events == [WeeklyEvent(title="comment", weekday=1)]


def test_empty_description_will_cause_early_exit() -> None:
    db = DB()

    with disable_print():
        with patch("builtins.input") as p:
            p.side_effect = [""]

            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2

    assert not db.events


def test_empty_event_format_will_cause_early_exit() -> None:
    db = DB()

    with disable_print():
        with patch("builtins.input") as p:
            p.side_effect = ["comment", ""]

            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2

    assert not db.events


def test_move_up_and_down_in_event_list() -> None:
    db = DB(events=[WeeklyEvent("abc", 0), WeeklyEvent("xyz", 1)])
    kb = keyboard([Keys.DOWN, Keys.UP, Keys.QUIT])

    with disable_print():
        states = list(recurring_event_manager(db, kb))

    assert len(states) == 3

    assert Colors.SELECTED.colorize(f"* {db.events[0]}") in states[0]
    assert Colors.SELECTED.colorize(f"* {db.events[1]}") in states[1]


def test_delete_event_from_event_list() -> None:
    event = WeeklyEvent("abc", 0)
    db = DB(events=[event])
    kb = keyboard([Keys.DELETE, Keys.QUIT])

    with disable_print():
        states = list(recurring_event_manager(db, kb))

    assert len(states) == 2

    assert Colors.SELECTED.colorize(f"* {event}") in states[0]

    assert str(event) not in states[1]
    assert not db.events


def test_delete_item_from_end_of_list_decrements_index() -> None:
    event = WeeklyEvent("abc", 0)
    db = DB(events=[event, WeeklyEvent("xyz", 1)])
    kb = keyboard([Keys.DOWN, Keys.DELETE, Keys.QUIT])

    with disable_print():
        states = list(recurring_event_manager(db, kb))

    assert len(states) == 3

    assert Colors.SELECTED.colorize(f"* {event}") in states[2]

    assert db.events == [event]


def test_cannot_go_above_topmost_event() -> None:
    event = WeeklyEvent("abc", 0)
    db = DB(events=[event])
    kb = keyboard([Keys.UP, Keys.UP, Keys.UP, Keys.QUIT])

    with disable_print():
        states = list(recurring_event_manager(db, kb))

    assert len(states) == 4

    for state in states[3:]:
        assert Colors.SELECTED.colorize(f"* {event}") in state


def test_cannot_go_below_lowest_event() -> None:
    event = WeeklyEvent("abc", 0)
    db = DB(events=[event])
    kb = keyboard([Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.QUIT])

    with disable_print():
        states = list(recurring_event_manager(db, kb))

    assert len(states) == 4

    for state in states[3:]:
        assert Colors.SELECTED.colorize(f"* {event}") in state
