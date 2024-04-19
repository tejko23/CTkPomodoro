import pytest

from pomodoro import Model, Timer


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
    assert model.timer.time == Model().timer.time
    assert model.timer.time == Timer(model._settings_time).time


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
