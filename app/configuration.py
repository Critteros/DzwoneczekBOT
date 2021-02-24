"""
Managing global-wide app configuration
"""

# Library includes
from enum import Enum
from pathlib import Path
import json

# import logging
# logging.DEBUG


# Constants
_DEFAULT_CONFIG_PATH = 'app/default_config.json'
_CONFIG_PATH = 'config.json'


class Config:
    """
    Class that holds app configuration

    Fields [Possible Values]:
        log_to_console  [true/false]
        log_to_file     [true/false]
        log_library     [true/false]

        console_log_level [DEBUG/INFO/WARNING/ERROR/CRITICAL]
        file_log_level    [DEBUG/INFO/WARNING/ERROR/CRITICAL]
        library_log_level [DEBUG/INFO/WARNING/ERROR/CRITICAL]

        console_use_color  [true/false]
        library_logging_type [CONSOLE/FILE]

        command_prefix      [char]

    """

    attributes: list = [
        'log_to_console',
        'log_to_file',
        'log_library',
        'console_log_level',
        'file_log_level',
        'library_log_level',
        'console_use_color',
        'library_logging_type',
        'command_prefix'
    ]

    def __init__(self, configuration: dict) -> None:

        try:
            self.log_to_console: bool = configuration['log_to_console']
            self.log_to_file: bool = configuration['log_to_file']
            self.log_library: bool = configuration['log_library']

            self.console_log_level: int = LoggingLevels[configuration['console_log_level']].value
            self.file_log_level: int = LoggingLevels[configuration['file_log_level']].value
            self.library_log_level: int = LoggingLevels[configuration['library_log_level']].value

            self.console_use_color: bool = configuration['console_use_color']
            self.library_logging_type: int = LogOutputType[
                configuration['library_logging_type']].value

            self.command_prefix: str = configuration['command_prefix']

        except KeyError as exc:
            raise ConfigAttributeNotFound from exc


# Configuration holders
_app_configuration: Config = None
_default_configuration: Config = None


def _load_config() -> dict:
    """
    Loads app configuration from 'config.json' file and returns it as a python dicitonary
    if the file is not found then it is created from a default config file. Raises error when
    json parser couldn't parse the file

    Raises:
        JsonDecodeError: Raised when JSON parser coudn't parse the file

    Returns:
        dict: The config as a python dictionary
    """
    file_object = Path(_CONFIG_PATH)

    # What to do if config does not exists
    if not file_object.exists():
        file_object.touch()
        json_data: dict = _load_default_config()

        # Creates config from default config
        with file_object.open('wt', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4)

        return json_data

    with file_object.open('rt', encoding='utf-8') as file:
        try:
            json_data = json.load(file)
        except json.JSONDecodeError as exc:
            raise JsonDecodeError(file_object.name) from exc

    return json_data


def _load_default_config() -> dict:
    """
    Loads default config file from disk to a python dictionary

    Raises:
        JsonDecodeError: Raised when JSON parser couldn't parse the JSON
        DefaultConfigNotFound: Raised when the default config is missing

    Returns:
        dict: Configuration as python dictionary
    """
    file_object = Path(_DEFAULT_CONFIG_PATH)

    try:
        assert file_object.exists()
    except AssertionError as exc:
        raise DefaultConfigNotFound(file_object.resolve()) from exc

    with file_object.open(mode='rt', encoding='utf-8') as file:
        try:
            json_data = json.load(file)
        except json.JSONDecodeError as exc:
            raise JsonDecodeError(file_object.name) from exc

    return json_data


class ConfigAttributeNotFound(Exception):
    """
    Raised when one of the config attribute is not found when creating instance of
    Config class

    """

    def __init__(self):
        super().__init__(
            'One of the required config attribute is missing when creating Config instance')


class DefaultConfigNotFound(Exception):
    """
    Raised when Default Configuration file is not found

    """

    def __init__(self, filepath: str):
        message = f'Default config should be at {filepath} but was not found!'
        super().__init__(message)


class JsonDecodeError(Exception):
    """
    Exception raised when trying to decode invalid JSON file

    Attributes:
        filename - name of file in which JSON threw exception when decoding
    """

    def __init__(self, filename: str):
        message = f'Invalid json: {filename}'
        super().__init__(message)


class LogOutputType(Enum):
    """
    Enum that represents diffrent methods of writing log messages either to stdout in console
    or to use a file
    """
    CONSOLE = 0
    FILE = 1


class LoggingLevels(Enum):
    """
    Enum that represents conversion from string description of log level
    to int value that logging library describes that logging level

    """

    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


# print(Config(_load_default_config()).__dict__)
