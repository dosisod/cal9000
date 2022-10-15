from enum import Enum, auto


class State(Enum):
    NORMAL = auto()
    COUNT = auto()
    COMMAND = auto()
    SEARCH = auto()


ESCAPE = "\x1b"
BACKSPACE = "\x7f"


class CommandBar:
    state = State.NORMAL
    width = 0
    _cache = ""

    def __init__(self, width: int = 0) -> None:
        self.width = width

    def append(self, c: str) -> bool:
        if c == ESCAPE:
            self.state = State.NORMAL
            self._cache = ""

        elif c == ":" and self.state in (State.NORMAL, State.COMMAND):
            self.state = State.COMMAND
            self._cache += c

        elif c == "/" and self.state in (State.NORMAL, State.SEARCH):
            self.state = State.SEARCH
            self._cache += c

        elif self.state in (State.COMMAND, State.SEARCH):
            if c == BACKSPACE:
                self._cache = self._cache[:-1]

                if not self._cache:
                    self.state = State.NORMAL

            else:
                self._cache += c

        elif c.isdigit() and self.state in (State.NORMAL, State.COUNT):
            self.state = State.COUNT
            self._cache += c

        else:
            return False

        return True

    @property
    def count(self) -> int:
        return int(self._cache) if self.state == State.COUNT else 0

    @property
    def command(self) -> str:
        return self._cache if self.state == State.COMMAND else ""

    @property
    def search(self) -> str:
        return self._cache if self.state == State.SEARCH else ""

    def __str__(self) -> str:
        if not self.width:
            return ""

        if count := self.count:
            return f"{count:>{self.width}}"

        if search := self.search:
            return f"{search:<{self.width}}"

        if command := self.command:
            return f"{command:<{self.width}}"

        return ""

    def reset(self) -> None:
        self.state = State.NORMAL
        self._cache = ""
