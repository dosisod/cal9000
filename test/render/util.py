from contextlib import contextmanager
from unittest.mock import patch


class keyboard:
    keys: list[str]

    def __init__(self, keys: list[str]) -> None:
        self.keys = keys

    def __call__(self) -> str:
        return self.keys.pop(0)


@contextmanager
def disable_print():
    with (
        patch("builtins.print"),
        patch("cal9000.ui.restore_old_termios_flags"),
        patch("cal9000.ui.restore_new_termios_flags"),
    ):
        yield
