# cal9000

Vim enabled version of [cal(1)](https://linux.die.net/man/1/cal).

## Why?

I want to get better about using calendars, but I don't like the thought of
using an online one. I also wanted something that I could use from the CLI
with ease, and be very effecient with it.

## Installing and Running

```
$ pip install cal9000
$ cal9000
```

## Usage

In short, the following Vim keybindings are supported:

| Key(s)     | Action |
|------------|--------|
| `q`        | Quit |
| `h`        | Go to previous day |
| `j`        | Go to next week |
| `J`        | Go 4 weeks forward |
| `k`        | Go to last week |
| `K`        | Go 4 weeks back |
| `l`        | Go to next day |
| `u`        | Go to to today |
| `i`        | Insert an item/event |
| `x`        | Delete an event or item |
| `g`        | Open event manager |
| `o`        | Open the selected day |
| `?`        | Open help menu |
| `:command` | Run the command `command`, see below for supported commands |
| *count*`verb` | Run `verb` (`h`/`j`/`k`/`l`, etc) `count` times |

## Commands

Currently supported commands are:

| Command       | Description |
|---------------|-------------|
| `h` or `help` | Open help dialog |
| `q` or `quit` | Quit cal9000 |
| *number*      | Go to day *number* of the current month |

## Configuration

TBD

## Testing

```
$ git clone https://github.com/dosisod/cal9000
$ cd cal9000
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip3 install -r dev-requirements.txt
```
