import calendar
from dataclasses import dataclass
from datetime import datetime

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

    def is_on_date(self, date: datetime) -> bool:
        raise NotImplementedError  # pragma: no cover


@dataclass
class MonthlyEvent(Event):
    day: int

    def __str__(self) -> str:
        suffix = day_suffix(self.day)

        return f"{self.title} ({self.day}{suffix} of every month)"

    def is_on_date(self, date: datetime) -> bool:
        return self.day == date.day


@dataclass
class WeeklyEvent(Event):
    weekday: int

    def __str__(self) -> str:
        weekday = WEEK_DAY_NAMES[self.weekday].title()

        return f"{self.title} (every {weekday})"

    def is_on_date(self, date: datetime) -> bool:
        return self.weekday == (date.isoweekday() % 7)


@dataclass
class YearlyEvent(Event):
    month: int
    day: int

    def __str__(self) -> str:
        month = calendar.month_name[self.month]
        day = f"{self.day}{day_suffix(self.day)}"

        return f"{self.title} ({month} {day})"

    def is_on_date(self, date: datetime) -> bool:
        return self.month == date.month and self.day == date.day
