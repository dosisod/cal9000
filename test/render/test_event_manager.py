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
    inserting = "1st of every month # comment"

    with disable_print():
        with patch("builtins.input", lambda _: inserting):
            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2
    assert "comment" in states[1]

    assert db.events == [MonthlyEvent("comment", day=1)]


def test_insert_weekly_event() -> None:
    db = DB()
    inserting = "every sunday # comment"

    with disable_print():
        with patch("builtins.input", lambda _: inserting):
            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2
    assert "comment" in states[1]

    assert db.events == [WeeklyEvent("comment", weekday=0)]


def test_invalid_weekly_event_doest_cause_error() -> None:
    db = DB()
    inserting = "every invalid_weekday # comment"

    with disable_print():
        with patch("builtins.input", lambda _: inserting):
            kb = keyboard([Keys.INSERT, Keys.QUIT])
            states = list(recurring_event_manager(db, kb))

    assert len(states) == 2
    assert "comment" not in states[1]

    assert not db.events
