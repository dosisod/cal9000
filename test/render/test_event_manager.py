from unittest.mock import patch

from cal9000.config import Keys
from cal9000.events import MonthlyEvent, WeeklyEvent
from cal9000.io import DB
from cal9000.render.event_manager import recurring_event_manager, render_events

from .util import disable_print, keyboard


def test_render_events() -> None:
    event = MonthlyEvent(title="some title", day=1)
    got = render_events([event])

    expected = f"""\
Recurring events:

* {str(event)}"""

    assert got == expected


def test_render_events_with_no_events() -> None:
    got = render_events([])

    expected = "Recurring events:\n\nNo recurring events"

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
