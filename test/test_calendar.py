from datetime import datetime
from unittest.mock import patch

from cal9000.config import Colors
from cal9000.events import MonthlyEvent, WeeklyEvent
from cal9000.io import DB, Items
from cal9000.render.calendar import (
    get_calendar_grid,
    render_calendar,
    render_calendar_cell,
    render_calendar_month_title,
)


def test_render_calendar_title() -> None:
    expected = {
        1: "    January 2022    ",
        2: "    February 2022   ",
        3: "     March 2022     ",
        4: "     April 2022     ",
        5: "      May 2022      ",
        6: "      June 2022     ",
        7: "      July 2022     ",
        8: "     August 2022    ",
        9: "   September 2022   ",
        10: "    October 2022    ",
        11: "    November 2022   ",
        12: "    December 2022   ",
    }

    for month, title in expected.items():
        date = datetime(month=month, year=2022, day=1)
        got = render_calendar_month_title(date)

        assert got == title


def test_render_calendar_cell_empty() -> None:
    assert render_calendar_cell(0) == "  "


def test_render_calendar_single_digit() -> None:
    assert render_calendar_cell(1) == " 1"


def test_render_calendar_double_digit() -> None:
    assert render_calendar_cell(12) == "12"


def test_render_calendar_when_selected() -> None:
    got = render_calendar_cell(12, Colors.SELECTED)
    expected = Colors.SELECTED.colorize("12")

    assert got == expected


def test_render_calendar_when_item_is_present() -> None:
    got = render_calendar_cell(12, Colors.HAS_ITEM)
    expected = Colors.HAS_ITEM.colorize("12")

    assert got == expected


def test_get_calendar_grid() -> None:
    assert get_calendar_grid(datetime(day=1, month=7, year=2022)) == [
        [0, 0, 0, 0, 0, 1, 2],
        [3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15, 16],
        [17, 18, 19, 20, 21, 22, 23],
        [24, 25, 26, 27, 28, 29, 30],
        [31, 0, 0, 0, 0, 0, 0],
    ]


def colorize_visualizer(self: Colors, text: str) -> str:
    if self == Colors.SELECTED:
        return "xx"
    if self == Colors.HAS_ITEM:
        return "--"

    return text


def test_render_calendar() -> None:
    date = datetime(day=1, month=7, year=2022)

    with patch("cal9000.config.Colors.colorize", colorize_visualizer):
        got = render_calendar(date, DB())

    expected = """\
      July 2022     
Su Mo Tu We Th Fr Sa
               xx  2
 3  4  5  6  7  8  9
10 11 12 13 14 15 16
17 18 19 20 21 22 23
24 25 26 27 28 29 30
31                  """

    assert expected == got


def test_render_calendar_with_events_present() -> None:
    date = datetime(day=1, month=7, year=2022)
    monthly_event = MonthlyEvent(day=8, title="")
    weekly_event = WeeklyEvent(weekday=1, title="")
    db = DB(events=[monthly_event, weekly_event])

    with patch("cal9000.config.Colors.colorize", colorize_visualizer):
        got = render_calendar(date, db)

    expected = """\
      July 2022     
Su Mo Tu We Th Fr Sa
               xx  2
 3 --  5  6  7 --  9
10 -- 12 13 14 15 16
17 -- 19 20 21 22 23
24 -- 26 27 28 29 30
31                  """

    assert expected == got


def test_render_calendar_when_daily_item_present() -> None:
    selected_date = datetime(month=12, day=20, year=2022)
    item_date = datetime(month=12, day=19, year=2022)
    items = {item_date.strftime("%s"): ["item 1", "item 2"]}
    db = DB(items=Items(list, items))

    with patch("cal9000.config.Colors.colorize", colorize_visualizer):
        got = render_calendar(selected_date, db)

    expected = """\
    December 2022   
Su Mo Tu We Th Fr Sa
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 -- xx 21 22 23 24
25 26 27 28 29 30 31"""

    assert expected == got
