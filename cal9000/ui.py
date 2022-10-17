import termios
from contextlib import contextmanager
from typing import Any, Generator

__old_flags: list[Any]  # type: ignore
__flags: list[Any]  # type: ignore

View = Generator[str, None, None]


def hide_cursor() -> None:
    print("\x1b[?25l", end="")


def show_cursor() -> None:
    print("\x1b[?25h", end="")


def save_cursor_pos() -> None:
    print("\x1b[s", end="")


def restore_cursor_pos() -> None:
    print("\x1b[u", end="")


def clear_line_and_below() -> None:
    print("\x1b[J", end="")


def clear_screen() -> None:
    print("\x1b[2J", end="")


def cursor_set_pos(row: int = 1, col: int = 1) -> None:
    print(f"\x1b[{row};{col}H", end="")


def move_n_lines_up(lines: int) -> None:
    print(f"\x1b[{lines}A", end="")


def setup_termios() -> None:
    global __old_flags, __flags
    __flags = termios.tcgetattr(0)
    __old_flags = __flags.copy()
    __flags[3] &= ~(termios.ICANON | termios.ECHO)
    restore_new_termios_flags()


def restore_old_termios_flags() -> None:
    global __old_flags
    termios.tcsetattr(0, 0, __old_flags)


def restore_new_termios_flags() -> None:
    global __old_flags, __flags
    termios.tcsetattr(0, 0, __flags)


def ensure_n_lines_below(lines: int) -> None:
    lines -= 1

    print("\n" * lines, end="")
    move_n_lines_up(lines)


@contextmanager
def ui_window(full_reset: bool = False) -> Generator[None, None, None]:
    clear_line_and_below()

    if full_reset:
        restore_old_termios_flags()
        show_cursor()
        yield
        hide_cursor()
        restore_new_termios_flags()

    else:
        yield

    restore_cursor_pos()


@contextmanager
def root_window() -> Generator[None, None, None]:
    setup_termios()
    restore_new_termios_flags()
    ensure_n_lines_below(9)
    save_cursor_pos()
    hide_cursor()

    try:
        yield

    except KeyboardInterrupt:
        pass

    finally:
        clear_line_and_below()
        show_cursor()
        restore_old_termios_flags()
