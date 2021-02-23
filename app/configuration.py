"""
Managing global-wide app configuration
"""

# Library includes
from enum import Enum

# import logging
# logging.DEBUG

# Configuration holders


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
