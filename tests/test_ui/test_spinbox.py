import pytest
from .mocks import AppMock

from pomodoro.ui.spinbox import Spinbox


@pytest.fixture
def spinbox() -> Spinbox:
    return Spinbox(
        master=AppMock(),
        entry="10",
        step_size=1,
        command=lambda: print("Test"),
    )


def test_add_button_callback(spinbox: Spinbox) -> None:
    for _ in range(60):
        spinbox.add_button_callback()
    assert spinbox.get() == "60"


def test_add_button_callback_raises_value_error(spinbox: Spinbox) -> None:
    spinbox.entry.configure(text="Value")
    with pytest.raises(ValueError):
        spinbox.add_button_callback()


def test_subtract_button_callback(spinbox: Spinbox) -> None:
    for _ in range(15):
        spinbox.subtract_button_callback()
    assert spinbox.get() == "1"


def test_subtract_button_callback_raises_value_error(spinbox: Spinbox) -> None:
    spinbox.entry.configure(text="Value")
    with pytest.raises(ValueError):
        spinbox.subtract_button_callback()
