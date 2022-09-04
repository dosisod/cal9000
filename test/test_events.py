from cal9000.events import Event, MonthlyEvent, WeeklyEvent, day_suffix


def test_day_suffixes() -> None:
    days = {
        1: "st",
        2: "nd",
        3: "rd",
        4: "th",
        5: "th",
        6: "th",
        7: "th",
        8: "th",
        9: "th",
        10: "th",
        11: "th",
        12: "th",
        13: "th",
        14: "th",
        15: "th",
        16: "th",
        17: "th",
        18: "th",
        19: "th",
        20: "th",
        21: "st",
        22: "nd",
        23: "rd",
        24: "th",
        25: "th",
        26: "th",
        27: "th",
        28: "th",
        29: "th",
        30: "th",
        31: "st",
    }

    for day, suffix in days.items():
        assert day_suffix(day) == suffix


def test_create_event() -> None:
    event = Event(title="something")

    assert event.title == str(event) == "something"


def test_create_monthly_event() -> None:
    event = MonthlyEvent(title="something", day=1)

    assert event.title == "something"
    assert event.day == 1
    assert str(event) == "something (1st of every month)"


def test_create_weekly_event() -> None:
    event = WeeklyEvent(title="something", weekday=0)

    assert event.title == "something"
    assert event.weekday == 0
    assert str(event) == "something (every Sunday)"
