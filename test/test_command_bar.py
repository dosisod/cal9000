from cal9000.command_bar import BACKSPACE, ESCAPE, CommandBar


def test_numbers_increments_count() -> None:
    cmd_bar = CommandBar()

    assert cmd_bar.append("1")
    assert cmd_bar.append("2")
    assert cmd_bar.append("3")

    assert cmd_bar.count == 123


def test_zero_is_allowed() -> None:
    cmd_bar = CommandBar()

    assert cmd_bar.append("0")
    assert cmd_bar.append("1")
    assert cmd_bar.append("0")

    assert cmd_bar.count == 10


def test_escape_will_clear_count() -> None:
    cmd_bar = CommandBar()

    assert cmd_bar.append("1")
    assert cmd_bar.append("0")
    assert cmd_bar.append("0")

    print(cmd_bar._cache)
    assert cmd_bar.count == 100

    cmd_bar.append(ESCAPE)

    assert cmd_bar.count == 0


def test_command_typing() -> None:
    cmd_bar = CommandBar()

    statuses = [
        cmd_bar.append(":"),
        cmd_bar.append("h"),
        cmd_bar.append("e"),
        cmd_bar.append("l"),
        cmd_bar.append("p"),
    ]

    assert all(statuses)

    assert cmd_bar.command == ":help"


def test_escape_clears_command() -> None:
    cmd_bar = CommandBar()

    cmd_bar.append(":")
    cmd_bar.append("x")

    assert cmd_bar.command == ":x"

    assert cmd_bar.append(ESCAPE)

    assert not cmd_bar.command


def test_numbers_in_command_doesnt_increase_count() -> None:
    cmd_bar = CommandBar()

    cmd_bar.append(":")
    cmd_bar.append("x")
    cmd_bar.append("1")

    assert cmd_bar.command == ":x1"
    assert cmd_bar.count == 0


def test_type_search() -> None:
    cmd_bar = CommandBar()

    assert cmd_bar.append("/")
    assert cmd_bar.append("x")
    assert cmd_bar.append("y")
    assert cmd_bar.append("z")

    assert cmd_bar.search == "/xyz"


def test_escape_cancels_search() -> None:
    cmd_bar = CommandBar()

    cmd_bar.append("/")
    cmd_bar.append("x")
    cmd_bar.append("y")
    cmd_bar.append("z")

    assert cmd_bar.search == "/xyz"

    assert cmd_bar.append(ESCAPE)

    assert cmd_bar.search == ""


def test_cannot_move_from_count_to_escape_or_command() -> None:
    cmd_bar = CommandBar()

    cmd_bar.append("1")

    assert cmd_bar.count == 1

    assert not cmd_bar.append("/")
    assert not cmd_bar.append(":")
    assert cmd_bar.count == 1


def test_display_command_bar() -> None:
    tests = {
        "1": "         1",
        "123": "       123",
        ":abc": ":abc      ",
        "/xyz": "/xyz      ",
    }

    for text, expected in tests.items():
        cmd_bar = CommandBar(width=10)

        for c in text:
            cmd_bar.append(c)

        assert str(cmd_bar) == expected


def test_backspace_removes_last_char() -> None:
    cmd_bar = CommandBar()

    for c in ":xyz" + BACKSPACE:
        cmd_bar.append(c)

    assert cmd_bar.command == ":xy"


def test_backspace_whole_line_resets_mode() -> None:
    cmd_bar = CommandBar()

    for c in f":abc{BACKSPACE * 4}/xyz":
        cmd_bar.append(c)

    assert not cmd_bar.command
    assert cmd_bar.search == "/xyz"


def test_reset() -> None:
    cmd_bar = CommandBar()

    for c in ":abc":
        cmd_bar.append(c)

    assert cmd_bar.command == ":abc"

    cmd_bar.reset()

    assert not cmd_bar.command


def test_zero_width_bar_displays_nothing() -> None:
    assert str(CommandBar()) == ""
