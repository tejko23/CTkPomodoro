import pytest
from typing import Callable

from pomodoro import Model, PomodoroPresenter
from pomodoro.model.settings import ConfigManager


class ViewMock:
    def mainloop(self) -> None: ...

    def bell(self) -> None: ...

    def run_job(self, time_ms: int, func: Callable) -> None: ...

    def cancel_job(self) -> None: ...

    def init_ui(self, config: ConfigManager, time: str) -> None: ...

    def set_clock_label(self, time: str) -> None: ...

    def bind_button(self, type: str, fn: Callable) -> None: ...

    def bind_ss_button(self, fn: Callable) -> None: ...


@pytest.fixture
def presenter() -> PomodoroPresenter:
    return PomodoroPresenter(ViewMock(), Model())


def test_run_method(presenter: PomodoroPresenter) -> None:
    presenter.run()


def test_handle_stop_button(presenter: PomodoroPresenter) -> None:
    presenter.model.state.finish()
    presenter.handle_stop_button()
    assert presenter.model.state.is_stopped() == True


def test_handle_start_button(presenter: PomodoroPresenter) -> None:
    presenter.handle_start_button()
    assert presenter.model.state.is_running() == True


def test_set_time(presenter: PomodoroPresenter) -> None:
    presenter.set_time("pomodoro")


def test_pomodoro_method_model_started(presenter: PomodoroPresenter) -> None:
    presenter.model.start_timer()
    presenter.pomodoro()


def test_pomodoro_method_model_finished(presenter: PomodoroPresenter) -> None:
    presenter.model.state.finish()
    presenter.pomodoro()


def test_pomodoro_method_model_stopped(presenter: PomodoroPresenter) -> None:
    presenter.model.stop_timer()
    presenter.pomodoro()


def test_update_running_state(presenter: PomodoroPresenter) -> None:
    presenter._update_running_state()


def test_trigger_alert_on_finished_state(presenter: PomodoroPresenter) -> None:
    presenter._trigger_alert_on_finished_state()


def test_handle_stopped_state(presenter: PomodoroPresenter) -> None:
    presenter._handle_stopped_state()
