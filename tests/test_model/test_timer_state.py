from pomodoro import TimerState


def test_running() -> None:
    assert TimerState.RUNNING.value == "running"


def test_stopped() -> None:
    assert TimerState.STOPPED.value == "stopped"


def test_finished() -> None:
    assert TimerState.FINISHED.value == "finished"
