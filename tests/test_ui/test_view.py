import pytest

from pomodoro import Pomodoro


class ConfigMock:
    pass


@pytest.fixture
def view() -> Pomodoro:
    return Pomodoro()


def test_init_ui(view: Pomodoro) -> None:
    view.init_ui(ConfigMock(), "10:00")


def test_setting_clock_label(view: Pomodoro) -> None:
    view.init_ui(ConfigMock(), "10:00")
    view.set_clock_label("05:00")
    assert view.clock.time == "05:00"


def test_binding_update_button(view: Pomodoro) -> None:
    view.init_ui(ConfigMock(), "10:00")
    view.bind_update_button(lambda: 10)
