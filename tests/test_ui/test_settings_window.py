import pytest
from unittest.mock import Mock

from .mocks import AppMock
from pomodoro.ui.settings import SettingsWindow


@pytest.fixture
def settings() -> SettingsWindow:
    return SettingsWindow(presenter=Mock(), master=AppMock(), config=Mock())


def test_save_to_config_method(settings: SettingsWindow) -> None:
    settings.withdraw()
    settings._save_to_config("break_time")


def test_set_interval_method(settings: SettingsWindow) -> None:
    settings.withdraw()
    settings._set_interval()
