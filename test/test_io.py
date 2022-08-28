from collections import defaultdict
from pathlib import Path
import json

from cal9000.io import DB, Items, load_save_file, save_items
from cal9000.events import Event


def test_load_save_file_doesnt_exist_will_return_empty_store():
    db = load_save_file("file that doesnt exist")

    assert len(db.items) == 0
    assert len(db.events) == 0


def test_load_save_file_loads_file_correctly_if_exists(tmp_path: str):
    save_file = Path(tmp_path) / "file.json"
    save_file.write_text(
        r'{"items":{"123456":["item 1", "item 2", "item 3"]},"events":[]}'
    )

    db = load_save_file(str(save_file))

    assert isinstance(db.items, defaultdict)
    assert db.items == {"123456": ["item 1", "item 2", "item 3"]}


def test_save_items(tmp_path: str):
    save_file = Path(tmp_path) / "file.json"

    items = {"123": ["item 1"]}
    events = [Event("something")]
    db = DB(items=Items(list, items), events=events)

    assert not save_file.exists()

    save_items(db, str(save_file))

    assert save_file.exists()
    assert save_file.read_text() == json.dumps(db.to_json())
