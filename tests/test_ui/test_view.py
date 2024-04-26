import pytest
from unittest.mock import Mock, patch


from .mocks import ButtonMock, ClockMock, SettingsWindowMock, AppMock
from pomodoro import Pomodoro
from pomodoro.ui.view import SettingsWindowFactory, ClockFrame, AppHeaderFrame


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
    with patch("pomodoro.ui.view.AppHeaderFrame", return_value=Mock()):
        view.init_ui(presenter=Mock(), config=Mock(), time="10:00")


def test_setting_clock_label(view: Pomodoro) -> None:
    with pytest.raises(TypeError):
        view.set_clock_label("05:00")
    view.clock = ClockMock(view)
    view.set_clock_label("05:00")
    assert view.clock.time == "05:00"


def test_bind_time_type_button_raises_attribute_error(view: Pomodoro) -> None:
    with pytest.raises(AttributeError):
        view.bind_time_type_button("pomodoro", lambda: "Test")


def test_set_border_for_type_buttons(view: Pomodoro) -> None:
    with patch("pomodoro.ui.view.AppHeaderFrame", return_value=Mock()):
        view.init_ui(presenter=Mock(), config=Mock(), time="10:00")
    view.set_border_for_type_buttons("break")


def test_set_border_for_type_buttons_raises_value_error(
    view: Pomodoro,
) -> None:
    with pytest.raises(ValueError):
        view.set_border_for_type_buttons("invalid_value")


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
    view.pomodoro_time_btn = ButtonMock()
    view.break_time_btn = ButtonMock()
    view.long_break_time_btn = ButtonMock()
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
    with patch("pomodoro.ui.view.AppHeaderFrame", return_value=Mock()):
        view.init_ui(presenter=Mock(), config=Mock(), time="10:00")
    view.open_settings_window()
    assert view.settings_window.focus() == "Mocked window focused"
    assert view.settings_window is not None
    assert isinstance(view.settings_window, SettingsWindowMock)


def test_open_settings_window_focuses_existing(view: Pomodoro) -> None:
    with patch("pomodoro.ui.view.AppHeaderFrame", return_value=Mock()):
        view.init_ui(presenter=Mock(), config=Mock(), time="10:00")
    view.settings_window = view.settings_window_factory.create_settings_window(
        master=view,
        presenter=view.presenter,
        config=view.config,
    )
    view.open_settings_window()
    assert hasattr(view.settings_window, "focus")


def test_create_settings_window() -> None:
    factory = SettingsWindowFactory(SettingsWindowMock)
    settings_window = factory.create_settings_window(
        master=Mock(), presenter=Mock(), config=Mock()
    )
    assert settings_window is not None


def test_clock_frame_time_property(clock: ClockFrame) -> None:
    assert clock.time == "10:00"


def test_clock_frame_time_setter(clock: ClockFrame) -> None:
    clock.time = "07:30"
    assert clock.time == "07:30"


def test_app_header_frame() -> None:
    with patch(
        "pomodoro.ui.view.customtkinter.CTkLabel",
        return_value=Mock(),
    ):
        AppHeaderFrame(master=AppMock(), command=Mock())
