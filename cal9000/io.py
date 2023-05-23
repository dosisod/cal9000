import json
from collections import defaultdict
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .events import Event, MonthlyEvent, WeeklyEvent, YearlyEvent

Keyboard = Callable[[], str]


@dataclass
class Item:
    data: str
    complete: bool = False

    def __str__(self) -> str:
        return self.data


Items = defaultdict[str, list[Item]]

DEFAULT_CONFIG_FILE = "~/.local/share/cal9000.json"


@dataclass
class DB:
    items: Items = field(default_factory=Items)
    events: list[Event] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:  # type: ignore
        return {
            "items": {
                k: [asdict(i) for i in v] for k, v in self.items.items()
            },
            "events": [asdict(e) for e in self.events],
        }


def load_save_file(filename: str = DEFAULT_CONFIG_FILE) -> DB:
    try:
        data = json.loads(Path(filename).expanduser().read_text())

        items = data["items"]
        events = data["events"]

    except (FileNotFoundError, KeyError):
        items = {}
        events = []

    def convert_event_from_json(event: dict[str, str | int]) -> Event:
        match event:
            case {"title": str(title), "month": int(month), "day": int(day)}:
                return YearlyEvent(title, month, day)

            case {"title": str(title), "day": int(day)}:
                return MonthlyEvent(title, day)

            case {"title": str(title), "weekday": int(weekday)}:
                return WeeklyEvent(title, weekday)

            case {"title": str(title)}:
                return Event(title)

            case _:
                raise ValueError("invalid event")

    def convert_items_from_json(item: str | dict[str, str | bool]) -> Item:
        match item:
            case str(data):
                return Item(data)

            case {"complete": bool(done), "data": str(data)}:
                return Item(data, done)

        raise ValueError("invalid item")  # pragma: no cover

    return DB(
        items=Items(
            list,
            {
                k: [convert_items_from_json(item) for item in v]
                for k, v in items.items()
            },
        ),
        events=[convert_event_from_json(e) for e in events],
    )


def save_items(db: DB, filename: str = DEFAULT_CONFIG_FILE) -> None:
    with Path(filename).expanduser().open("w+") as f:
        f.write(json.dumps(db.to_json(), separators=(",", ":")))
