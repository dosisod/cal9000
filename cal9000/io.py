from collections import defaultdict
from contextlib import suppress
from pathlib import Path
from typing import Callable
import json


Keyboard = Callable[[], str]

DEFAULT_CONFIG_FILE = "~/.local/share/cal9000.json"

Items = defaultdict[str, list[str]]


def load_save_file(filename: str = DEFAULT_CONFIG_FILE) -> Items:
    items = {}

    with suppress(FileNotFoundError):
        items = json.loads(Path(filename).expanduser().read_text())

    return defaultdict(list, items)


def save_items(items: Items, filename: str = DEFAULT_CONFIG_FILE) -> None:
    with Path(filename).expanduser().open("w+") as f:
        f.write(json.dumps(items))
