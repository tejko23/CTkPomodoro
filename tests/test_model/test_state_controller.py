import pytest

from pomodoro import StateController, TimerState


@pytest.fixture
def state_controller() -> StateController:
    return StateController()


def test_init_state_is_stopped(state_controller: StateController) -> None:
    state_controller.state == TimerState.STOPPED


def test_start(state_controller: StateController) -> None:
    state_controller.start()
    state_controller.state == TimerState.RUNNING


def test_stop(state_controller: StateController) -> None:
    state_controller.stop()
    state_controller.state == TimerState.STOPPED


def test_finish(state_controller: StateController) -> None:
    state_controller.finish()
    state_controller.state == TimerState.FINISHED


def test_is_running_method(state_controller: StateController) -> None:
    state_controller.is_running() == False
    state_controller.start()
    state_controller.is_running() == True


def test_is_stopped_method(state_controller: StateController) -> None:
    state_controller.is_stopped() == True
    state_controller.start()
    state_controller.is_stopped() == False


def test_is_finished_method(state_controller: StateController) -> None:
    state_controller.is_finished() == False
    state_controller.finish()
    state_controller.is_finished() == True
