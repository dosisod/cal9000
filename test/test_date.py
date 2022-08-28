from cal9000.date import get_today_date_only


def test_get_today_date_is_just_the_date_portion() -> None:
    date = get_today_date_only()

    assert not date.hour
    assert not date.minute
    assert not date.second
    assert not date.microsecond
