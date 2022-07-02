from collections import defaultdict
from pathlib import Path
import json

from cal9000.io import load_save_file, save_items


def test_load_save_file_doesnt_exist_will_return_empty_store():
    assert load_save_file("file that doesnt exist") == {}


def test_load_save_file_loads_file_correctly_if_exists(tmp_path: str):
    save_file = Path(tmp_path) / "file.json"
    save_file.write_text(r'{"123456":["item 1", "item 2", "item 3"]}')

    items = load_save_file(str(save_file))

    assert isinstance(items, defaultdict)
    assert items == {"123456": ["item 1", "item 2", "item 3"]}


def test_save_items(tmp_path: str):
    save_file = Path(tmp_path) / "file.json"

    items = {"123": ["item 1"]}

    assert not save_file.exists()

    save_items(defaultdict(list, items), str(save_file))

    assert save_file.exists()
    assert save_file.read_text() == json.dumps(items)
