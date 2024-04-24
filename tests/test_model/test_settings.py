import pytest
from configparser import NoSectionError
from pomodoro.model.settings import ConfigManager

TEST_CONFIG_FILE = ".\\tests\\test_model\\config.ini"


def create_test_config(content: str) -> None:
    """Creates a temporary config file for testing."""
    with open(TEST_CONFIG_FILE, "w") as f:
        f.write(content)


def remove_test_config() -> None:
    """Removes the temporary config file."""
    import os

    if os.path.exists(TEST_CONFIG_FILE):
        os.remove(TEST_CONFIG_FILE)


@pytest.fixture(scope="session", autouse=True)
def clean_test_config(request) -> None:
    """Ensures a clean test environment by removing any existing config file."""
    request.addfinalizer(remove_test_config)


@pytest.fixture
def config_manager() -> ConfigManager:
    return ConfigManager(TEST_CONFIG_FILE)


def test_init_no_config_file(config_manager) -> None:
    """Tests initialization without a config file."""
    assert config_manager.config.sections() == []


def test_init_with_config_file(config_manager) -> None:
    """Tests initialization with a valid config file."""
    content = "[Settings]\npomodoro_time=25"
    create_test_config(content)
    config_manager.config.read(TEST_CONFIG_FILE)
    assert config_manager.config.sections() == ["Settings"]


def test_set_param(config_manager) -> None:
    """Tests saving a parameter to the config file."""
    content = "[Settings]"
    create_test_config(content)
    config_manager._set_param("focus_time", "30")

    with open(TEST_CONFIG_FILE) as f:
        content = f.read()
    assert "focus_time = 30" in content


def test_get_param_existing(config_manager) -> None:
    """Tests loading an existing parameter from the config file."""
    content = "[Settings]\npomodoro_time=25"
    create_test_config(content)
    assert config_manager._get_param("pomodoro_time") == "25"


def test_get_param_nonexistent(config_manager) -> None:
    """Tests loading a non-existent parameter from the config file."""
    content = "[Settings]\n"
    create_test_config(content)
    with pytest.raises(KeyError):
        config_manager._get_param("nonexistent_param")


def test_get_pomodoro_time(config_manager) -> None:
    """Tests getting the 'pomodoro_time' parameter."""
    content = "[Settings]\npomodoro_time=25"
    create_test_config(content)
    assert config_manager.get_pomodoro_time() == "25"


def test_set_pomodoro_time(config_manager) -> None:
    """Tests setting the 'pomodoro_time' parameter."""
    content = "[Settings]\npomodoro_time=25"
    create_test_config(content)
    config_manager.set_pomodoro_time("30")
    assert config_manager.get_pomodoro_time() == "30"


def test_get_break_time(config_manager) -> None:
    """Tests getting the 'break_time' parameter."""
    content = "[Settings]\nbreak_time=5"
    create_test_config(content)
    assert config_manager.get_break_time() == "5"


def test_set_break_time(config_manager) -> None:
    """Tests setting the 'break_time' parameter."""
    content = "[Settings]\nbreak_time=5"
    create_test_config(content)
    config_manager.set_break_time("10")
    assert config_manager.get_break_time() == "10"


def test_get_long_break_time(config_manager) -> None:
    """Tests getting the 'long_break_time' parameter."""
    content = "[Settings]\nlong_break_time=15"
    create_test_config(content)
    assert config_manager.get_long_break_time() == "15"


def test_set_long_break_time(config_manager) -> None:
    """Tests setting the 'long_break_time' parameter."""
    content = "[Settings]\nlong_break_time=5"
    create_test_config(content)
    config_manager.set_long_break_time("20")
    assert config_manager.get_long_break_time() == "20"


def test_get_long_break_interval(config_manager) -> None:
    """Tests getting the 'long_break_interval' parameter."""
    content = "[Settings]\nlong_break_interval=3"
    create_test_config(content)
    assert config_manager.get_long_break_interval() == "3"


def test_set_long_break_interval(config_manager) -> None:
    """Tests setting the 'long_break_time' parameter."""
    content = "[Settings]\nlong_break_interval=3"
    create_test_config(content)
    config_manager.set_long_break_interval("4")
    assert config_manager.get_long_break_interval() == "4"
