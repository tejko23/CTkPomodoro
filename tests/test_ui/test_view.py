import pytest
from unittest.mock import Mock

from .mocks import (
    ButtonMock,
    ClockMock,
    SettingsWindowMock,
)
from pomodoro import Pomodoro
from pomodoro.ui.view import SettingsWindowFactory, ClockFrame


@pytest.fixture
def view() -> Pomodoro:
    return Pomodoro(
        settings_window_factory=SettingsWindowFactory(SettingsWindowMock)
    )


@pytest.fixture
def clock(view: Pomodoro) -> ClockFrame:
    view.clock = ClockFrame(view, time="10:00")
    return view.clock


def test_init_ui(view: Pomodoro) -> None:
    view.init_ui(Mock(), "10:00")


def test_setting_clock_label(view: Pomodoro) -> None:
    with pytest.raises(TypeError):
        view.set_clock_label("05:00")
    view.clock = ClockMock(view)
    view.set_clock_label("05:00")
    assert view.clock.time == "05:00"


def test_bind_update_button(view: Pomodoro) -> None:
    view.update_btn = ButtonMock()
    view.bind_update_button(lambda: "Test")


def test_bind_update_button_raises_type_error(view: Pomodoro) -> None:
    with pytest.raises(TypeError):
        view.bind_update_button(lambda: "Test")
    view.update_btn = ButtonMock()
    with pytest.raises(TypeError):
        view.bind_update_button("Test")


def test_bind_ss_button(view: Pomodoro) -> None:
    view.button = ButtonMock()
    view.bind_ss_button(lambda: "Test")


def test_bind_ss_button_raises_type_error(view: Pomodoro) -> None:
    with pytest.raises(TypeError):
        view.bind_ss_button(lambda: "Test")
    view.button = ButtonMock()
    with pytest.raises(TypeError):
        view.bind_ss_button("Test")


def test_swap_button_test_decorator(view: Pomodoro) -> None:
    view.button = ButtonMock()
    view.update_btn = ButtonMock()
    view.button.configure(text="Start")
    view.swap_button_text_decorator(lambda: "Test")
    view.button.configure(text="Stop")
    view.swap_button_text_decorator(lambda: "Test")


def test_run_job(view: Pomodoro) -> None:
    view.run_job(100, lambda: "Test")


def test_cancel_job(view: Pomodoro) -> None:
    view.run_job(100, lambda: "Test")
    view.cancel_job()


def test_open_settings_window_creates_new_window(view: Pomodoro) -> None:
    view.open_settings_window()
    assert view.settings_window.focus() == "Mocked window focused"
    assert view.settings_window is not None
    assert isinstance(view.settings_window, SettingsWindowMock)


def test_open_settings_window_focuses_existing(view: Pomodoro) -> None:
    view.settings_window = view.settings_window_factory.create_settings_window(
        master=view,
        config=view.config,
    )
    view.open_settings_window()
    assert hasattr(view.settings_window, "focus")


def test_create_settings_window() -> None:
    factory = SettingsWindowFactory(SettingsWindowMock)
    settings_window = factory.create_settings_window(
        master=Mock(), config=Mock()
    )
    assert settings_window is not None


def test_clock_frame_time_property(clock: ClockFrame) -> None:
    assert clock.time == "10:00"


def test_clock_frame_time_setter(clock: ClockFrame) -> None:
    clock.time = "07:30"
    assert clock.time == "07:30"
