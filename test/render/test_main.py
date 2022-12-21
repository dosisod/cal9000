from datetime import datetime
from test.render.util import disable_print, keyboard

from cal9000.config import Colors, Keys
from cal9000.io import DB
from cal9000.render.main import main


def test_main_show_help() -> None:
    kb = keyboard([Keys.HELP, Keys.QUIT, Keys.QUIT])
    date = datetime.now()

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 3
    assert "General help" in states[1]


def test_open_day() -> None:
    kb = keyboard([Keys.OPEN, Keys.QUIT, Keys.QUIT])
    date = datetime.now()

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 3
    assert "nothing for today" in states[1]


def test_calendar_go_up_then_home() -> None:
    kb = keyboard([Keys.UP, Keys.GO_HOME, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 3
    assert Colors.SELECTED.colorize(" 1") in states[0]
    assert Colors.SELECTED.colorize(" 1") not in states[1]
    assert Colors.SELECTED.colorize(" 1") in states[2]


def test_calendar_go_left() -> None:
    kb = keyboard([Keys.LEFT, Keys.QUIT])
    date = datetime(month=7, day=2, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert Colors.SELECTED.colorize(" 2") in states[0]
    assert Colors.SELECTED.colorize(" 1") in states[1]


def test_calendar_go_right() -> None:
    kb = keyboard([Keys.RIGHT, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert Colors.SELECTED.colorize(" 1") in states[0]
    assert Colors.SELECTED.colorize(" 2") in states[1]


def test_calendar_go_down() -> None:
    kb = keyboard([Keys.DOWN, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert Colors.SELECTED.colorize(" 1") in states[0]
    assert Colors.SELECTED.colorize(" 8") in states[1]


def test_calendar_go_up() -> None:
    kb = keyboard([Keys.UP, Keys.QUIT])
    date = datetime(month=7, day=8, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert Colors.SELECTED.colorize(" 8") in states[0]
    assert Colors.SELECTED.colorize(" 1") in states[1]


def test_calendar_go_up_4() -> None:
    kb = keyboard([Keys.UP_4, Keys.QUIT])
    date = datetime(month=7, day=29, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert Colors.SELECTED.colorize("29") in states[0]
    assert Colors.SELECTED.colorize(" 1") in states[1]


def test_calendar_go_down_4() -> None:
    kb = keyboard([Keys.DOWN_4, Keys.QUIT])
    date = datetime(month=7, day=1, year=2022)

    with disable_print():
        states = list(main(date, DB(), kb))

    assert len(states) == 2
    assert Colors.SELECTED.colorize(" 1") in states[0]
    assert Colors.SELECTED.colorize("29") in states[1]


def test_go_to_event_manager() -> None:
    kb = keyboard([Keys.GOTO_EVENTS, Keys.QUIT, Keys.QUIT])

    with disable_print():
        states = list(main(datetime.now(), DB(), kb))

    assert len(states) == 3
    assert "Recurring events" in states[1]


def command(cmd: str) -> list[str]:
    return list(f":{cmd}\n")


def test_help_command() -> None:
    for cmd in ("help", "h"):
        kb = keyboard(command(cmd) + ["\n", Keys.QUIT])

        with disable_print():
            states = list(main(datetime.now(), DB(), kb))

        assert "General help" in states[-2]


def test_goto_day_command() -> None:
    date = datetime(month=10, day=14, year=2022)
    kb = keyboard(command("15") + [Keys.QUIT])

    with disable_print():
        states = list(main(date, DB(), kb))

    assert Colors.SELECTED.colorize("15") in states[-1]


def test_goto_day_too_low_clamps_to_first_of_month() -> None:
    date = datetime(month=12, day=20, year=2022)
    kb = keyboard(command("0") + [Keys.QUIT])

    with disable_print():
        states = list(main(date, DB(), kb))

    assert Colors.SELECTED.colorize(" 1") in states[-1]


def test_goto_day_too_high_clamps_to_last_day_of_month() -> None:
    date = datetime(month=12, day=20, year=2022)
    kb = keyboard(command("999") + [Keys.QUIT])

    with disable_print():
        states = list(main(date, DB(), kb))

    assert Colors.SELECTED.colorize("31") in states[-1]


def test_apply_verb_count() -> None:
    date = datetime(month=10, day=14, year=2022)
    kb = keyboard(list("4h\n") + [Keys.QUIT])

    with disable_print():
        states = list(main(date, DB(), kb))

    assert Colors.SELECTED.colorize("10") in states[-1]


def test_command_bar_displayed_when_cmd_is_active() -> None:
    kb = keyboard(command("xyz") + [Keys.QUIT])

    with disable_print():
        states = list(main(datetime.now(), DB(), kb))

    assert ":xyz" in states[-2]


def test_quit_command() -> None:
    for cmd in ("quit", "q"):
        kb = keyboard(command(cmd))

        with disable_print():
            list(main(datetime.now(), DB(), kb))
