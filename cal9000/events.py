from dataclasses import dataclass

from cal9000.dates import WEEK_DAY_NAMES


# From: https://stackoverflow.com/a/52045942
def day_suffix(day: int) -> str:
    suffixes = ["th", "st", "nd", "rd"]

    if day % 10 in [1, 2, 3] and day not in [11, 12, 13]:
        return suffixes[day % 10]

    return suffixes[0]


@dataclass
class Event:
    title: str

    def __str__(self) -> str:
        return self.title


@dataclass
class MonthlyEvent(Event):
    day: int

    def __str__(self) -> str:
        suffix = day_suffix(self.day)

        return f"{self.title} ({self.day}{suffix} of every month)"


@dataclass
class WeeklyEvent(Event):
    weekday: int

    def __str__(self) -> str:
        weekday = WEEK_DAY_NAMES[self.weekday].title()

        return f"{self.title} (every {weekday})"
