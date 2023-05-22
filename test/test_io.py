import json
from collections import defaultdict
from pathlib import Path

import pytest

from cal9000.events import Event, MonthlyEvent, WeeklyEvent, YearlyEvent
from cal9000.io import DB, Items, load_save_file, save_items


def test_load_save_file_doesnt_exist_will_return_empty_store() -> None:
    db = load_save_file("file that doesnt exist")

    assert len(db.items) == 0
    assert len(db.events) == 0


def test_load_save_file_loads_file_correctly_if_exists(tmp_path: str) -> None:
    save_file = Path(tmp_path) / "file.json"
    save_file.write_text(
        r'{"items":{"123456":["item 1", "item 2", "item 3"]},"events":[]}'
    )

    db = load_save_file(str(save_file))

    assert isinstance(db.items, defaultdict)
    assert db.items == {"123456": ["item 1", "item 2", "item 3"]}


def test_load_save_file_save_events(tmp_path: str) -> None:
    save_file = Path(tmp_path) / "file.json"
    save_file.write_text(
        json.dumps(
            {
                "items": {},
                "events": [
                    {"title": "some yearly event", "month": 1, "day": 2},
                    {"title": "some monthly event", "day": 1},
                    {"title": "some weekly event", "weekday": 6},
                    {"title": "some normal event"},
                ],
            }
        )
    )

    db = load_save_file(str(save_file))

    assert db.events == [
        YearlyEvent(title="some yearly event", month=1, day=2),
        MonthlyEvent(title="some monthly event", day=1),
        WeeklyEvent(title="some weekly event", weekday=6),
        Event(title="some normal event"),
    ]


def test_load_save_file_fails_on_invalid_event(tmp_path: str) -> None:
    save_file = Path(tmp_path) / "file.json"
    save_file.write_text(
        json.dumps({"items": {}, "events": [{"invalid": "data"}]})
    )

    with pytest.raises(ValueError, match="invalid event"):
        load_save_file(str(save_file))


def test_save_items(tmp_path: str) -> None:
    save_file = Path(tmp_path) / "file.json"

    items = {"123": ["item 1"]}
    events = [Event("something")]
    db = DB(items=Items(list, items), events=events)

    assert not save_file.exists()

    save_items(db, str(save_file))

    assert save_file.exists()
    assert save_file.read_text() == json.dumps(db.to_json())
