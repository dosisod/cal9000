from cal9000.render.help import show_help
from test.render.util import disable_print, keyboard


def test_help_view():
    with disable_print():
        states = list(show_help(keyboard(["any key"])))

    assert len(states) == 1

    assert states[0]
