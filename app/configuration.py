"""
Managing global-wide app configuration
"""

# Library includes
from enum import Enum
from pathlib import Path
import json

# import logging
# logging.DEBUG

# Configuration holders
_app_configuration: dict = {}
_default_configuration: dict = {}

# Constants
_DEFAULT_CONFIG_PATH = 'app/default_config.json'


def _load_default_config() -> dict:
    file_object = Path(_DEFAULT_CONFIG_PATH)

    assert file_object.exists()

    with file_object.open(mode='rt') as file:
        try:
            json_data = json.load(file)
        except json.JSONDecodeError as exc:
            raise JsonDecodeError(file_object.name) from exc

    print(file_object.name)

    return json_data


class JsonDecodeError(Exception):
    """
    Exception raised when trying to decode invalid JSON file

    """

    def __init__(self, filename: str):
        message = f'Invalid json: {filename}'
        super().__init__(message)


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

        console_logger_type  [COLOR/NORMAL]
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
        'console_logger_type',
        'library_logging_type',
        'command_prefix'
    ]

    def __init__(self, configuration: dict) -> None:
        pass

    log_to_console: bool
    log_to_file: bool
    log_library: bool

    console_log_level: int
    file_log_level: int
    library_log_level: int

    console_logger_type: int
    library_logging_type: int

    command_prefix: str


class ConsoleOutputType(Enum):
    """
    Enum that represents diffrent methods of writing log messages either to stdout in console
    or to use a file
    """
    CONSOLE = 0
    FILE = 1


class ConsoleFormattingType(Enum):
    """
    Enum that represents methods of printing to color in nice color format or to just use
    plan white text. Converts string representationof state to integer state

    """
    NORMAL = 0
    COLOR = 1


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
