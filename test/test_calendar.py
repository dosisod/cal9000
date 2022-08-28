from datetime import datetime

from cal9000.render.calendar import (
    get_calendar_grid,
    invert_color,
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


def test_invert_color() -> None:
    assert invert_color("hello") == "\x1b[7mhello\x1b[0m"


def test_render_calendar_cell_empty() -> None:
    assert render_calendar_cell(0, False) == "  "


def test_render_calendar_single_digit() -> None:
    assert render_calendar_cell(1, False) == " 1"


def test_render_calendar_double_digit() -> None:
    assert render_calendar_cell(12, False) == "12"


def test_render_calendar_when_selected() -> None:
    assert render_calendar_cell(12, True) == invert_color("12")


def test_get_calendar_grid() -> None:
    assert get_calendar_grid(datetime(day=1, month=7, year=2022)) == [
        [0, 0, 0, 0, 0, 1, 2],
        [3, 4, 5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14, 15, 16],
        [17, 18, 19, 20, 21, 22, 23],
        [24, 25, 26, 27, 28, 29, 30],
        [31, 0, 0, 0, 0, 0, 0],
    ]


def test_render_calendar() -> None:
    date = datetime(day=1, month=7, year=2022)
    got = render_calendar(date)

    _1 = f" {invert_color(' 1')} "

    expected = f"""\
      July 2022     
Su Mo Tu We Th Fr Sa
              {_1} 2
 3  4  5  6  7  8  9
10 11 12 13 14 15 16
17 18 19 20 21 22 23
24 25 26 27 28 29 30
31                  """

    assert expected == got
