from enum import Enum


class Keys:
    QUIT = "q"
    LEFT = "h"
    RIGHT = "l"
    UP = "k"
    DOWN = "j"
    INSERT = "i"
    DOWN_4 = "J"
    UP_4 = "K"
    GO_HOME = "u"
    HELP = "?"
    OPEN = "o"
    DELETE = "x"
    GOTO_EVENTS = "g"


class Colors(Enum):
    SELECTED = "\x1b[1m\x1b[48;5;82m\x1b[38;5;237m{}\x1b[0m"
    HAS_ITEM = "\x1b[48;5;241m\x1b[38;5;232m{}\x1b[0m"

    def colorize(self, text: str) -> str:
        return self.value.format(text)
