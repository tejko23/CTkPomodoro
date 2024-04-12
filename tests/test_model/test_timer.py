from datetime import datetime, timedelta
import pytest

from pomodoro import Timer


@pytest.fixture
def timer() -> Timer:
    return Timer("10:00")


def test_timer_exists(timer: Timer) -> None:
    assert timer is not None


def test_time_str(timer: Timer) -> None:
    assert str(timer) == "10:00"


def test_time_property(timer: Timer) -> None:
    assert timer.time == "10:00"


def test_time_property_instance(timer: Timer) -> None:
    assert type(timer.time) == str


@pytest.mark.parametrize(
    "context, expected", (("5", "05:00"), ("06:30", "06:30"), ("0", "00:00"))
)
def test_time_setter(timer: Timer, context, expected) -> None:
    timer.time = context
    assert timer.time == expected


def test_time_setter_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Timer(10)


def test_time_setter_raises_value_error() -> None:
    with pytest.raises(ValueError):
        Timer("abc")


def test_refresh_end_time(timer: Timer) -> None:
    now = datetime.now()
    timer._time = timedelta(seconds=120)
    timer.set_end_time_to_correct()
    assert timer._end_time > now


def test_timer_state(timer: Timer) -> None:
    assert timer.state.is_running() == False


def test_calculate_time_method(timer: Timer) -> None:
    timer.set_end_time_to_correct()
    assert timer._calculate_time() == timedelta(minutes=10)


def test_calculate_time_method_while_running(timer: Timer) -> None:
    timer.set_end_time_to_correct()
    timer.state.start()
    two_minutes_ago = datetime.now() - timedelta(minutes=2)
    timer._end_time = two_minutes_ago + timer._time
    assert timer._calculate_time() == timedelta(minutes=8)


def test_timer_property_timer_running_before_end_time(timer: Timer) -> None:
    two_minutes_ago = datetime.now() - timedelta(minutes=2)
    timer._end_time = two_minutes_ago + timer._time
    timer.state.start()
    assert timer.time == "08:00"


def test_timer_property_timer_running_past_end_time(timer: Timer) -> None:
    timer.state.start()
    twenty_minutes_ago = datetime.now() - timedelta(minutes=20)
    timer._end_time = twenty_minutes_ago + timer._time
    assert timer.time == "00:00"
