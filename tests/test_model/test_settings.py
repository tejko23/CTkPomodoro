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


@pytest.fixture(autouse=True)
def clean_test_config() -> None:
    """Ensures a clean test environment by removing any existing config file."""
    remove_test_config()


@pytest.fixture
def config_manager() -> ConfigManager:
    return ConfigManager(TEST_CONFIG_FILE)


def test_init_no_config_file(config_manager, clean_test_config) -> None:
    """Tests initialization without a config file."""
    assert config_manager.config.sections() == []


def test_init_with_config_file(config_manager, clean_test_config) -> None:
    """Tests initialization with a valid config file."""
    content = "[Settings]\npomodoro_time=25"
    create_test_config(content)
    config_manager.config.read(TEST_CONFIG_FILE)
    assert config_manager.config.sections() == ["Settings"]


def test_save_param(config_manager, clean_test_config) -> None:
    """Tests saving a parameter to the config file."""
    content = "[Settings]"
    create_test_config(content)
    config_manager.save_param("focus_time", "30")

    with open(TEST_CONFIG_FILE) as f:
        content = f.read()
    assert "focus_time = 30" in content


def test_load_param_existing(config_manager, clean_test_config) -> None:
    """Tests loading an existing parameter from the config file."""
    content = "[Settings]\npomodoro_time=25"
    create_test_config(content)
    assert config_manager.load_param("pomodoro_time") == "25"


def test_load_param_nonexistent(config_manager, clean_test_config) -> None:
    """Tests loading a non-existent parameter from the config file."""
    content = "[Settings]\n"
    create_test_config(content)
    config_manager.config.read(TEST_CONFIG_FILE)
    with pytest.raises(KeyError):
        config_manager.load_param("nonexistent_param")


def test_get_pomodoro_time(config_manager, clean_test_config) -> None:
    """Tests getting the 'pomodoro_time' parameter."""
    content = "[Settings]\npomodoro_time=25"
    create_test_config(content)
    config_manager.config.read(TEST_CONFIG_FILE)
    assert config_manager.get_pomodoro_time() == "25"


def test_get_pomodoro_time_no_config_file(
    config_manager, clean_test_config
) -> None:
    """Tests getting 'pomodoro_time' when no config file exists."""
    with pytest.raises(KeyError):
        config_manager.get_pomodoro_time()
