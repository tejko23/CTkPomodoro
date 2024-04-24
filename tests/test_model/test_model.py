import pytest

from pomodoro import Model, Timer
from pomodoro.model import PomodoroSequence


@pytest.fixture
def model() -> Model:
    return Model()


def test_start_timer_method(model: Model) -> None:
    model.start_timer()
    assert model.state.is_running() == True
    assert model.state.is_stopped() == False
    assert model.state.is_finished() == False


def test_stop_timer_method(model: Model) -> None:
    model.start_timer()
    model.stop_timer()
    assert model.state.is_stopped() == True
    assert model.state.is_running() == False
    assert model.state.is_finished() == False


def test_reset_timer_method(model: Model) -> None:
    model.reset_timer()


def test_finish_timer_if_done(model: Model) -> None:
    model.timer.time = "00:00"
    model.start_timer()
    model.finish_timer_if_done()
    assert model.state.is_finished() == True
    assert model.state.is_stopped() == False
    assert model.state.is_running() == False

    model.timer.time = "05:00"
    model.start_timer()
    model.finish_timer_if_done()
    assert model.state.is_finished() == False
    assert model.state.is_stopped() == False
    assert model.state.is_running() == True


def test_set_time(model: Model) -> None:
    model.set_time("pomodoro")


def test_set_time_raise_value_error(model: Model) -> None:
    with pytest.raises(ValueError):
        model.set_time("something_wrong")


@pytest.fixture
def sequence() -> PomodoroSequence:
    return PomodoroSequence()


def test_sequence_valid_phase(sequence: PomodoroSequence):
    sequence._current = 0
    assert sequence._current == 0


def test_sequence_set_current_raises_value_error(
    sequence: PomodoroSequence, capsys
) -> None:
    sequence.set_current("invalid_phase")
    captured = capsys.readouterr()
    assert "invalid_phase is not a valid phase in the cycle." in captured.out


def test_sequence_set_interval(sequence: PomodoroSequence) -> None:
    sequence.set_interval(4)
