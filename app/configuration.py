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
        console_use_color  [true/false]

        console_log_level [DEBUG/INFO/WARNING/ERROR/CRITICAL]
        file_log_level    [DEBUG/INFO/WARNING/ERROR/CRITICAL]
        library_log_level [DEBUG/INFO/WARNING/ERROR/CRITICAL]


        library_logging_type [CONSOLE/FILE]

        command_prefix      [char]

    """

    def __init__(self, configuration: dict) -> None:
        """
        Initializes the config instance

        Args:
            configuration (dict): Configuration as dictionary
        """

        # log_to_console -
        #   bool [true/false] None if out of bounds or not found
        self.log_to_console: bool = configuration.get('log_to_console', None)

        # log_to_file -
        #   bool [true/false] None if out of bounds or not found
        self.log_to_file: bool = configuration.get('log_to_file', None)

        # log_library - bool [true/false] None if out of bounds or not found
        self.log_library: bool = configuration.get('log_library', None)

        # console_use_color - bool [true/false] None if out of bounds or not found
        self.console_use_color: bool = configuration.get(
            'console_use_color', None)

        # console_log_level -
        #   enum [DEBUG/INFO/WARNING/ERROR/CRITICAL] None if out of bounds or not found
        try:
            self.console_log_level: int = LoggingLevels[configuration['console_log_level']].value
        except KeyError:
            self.console_log_level: int = None

        # file_log_level -
        #   enum [DEBUG/INFO/WARNING/ERROR/CRITICAL] None if out of bounds or not found
        try:
            self.file_log_level: int = LoggingLevels[configuration['file_log_level']].value
        except KeyError:
            self.file_log_level: int = None

        # library_log_level -
        #   enum [DEBUG/INFO/WARNING/ERROR/CRITICAL] None if out of bounds or not found
        try:
            self.library_log_level: int = LoggingLevels[configuration['library_log_level']].value
        except KeyError:
            self.library_log_level: int = None

        # library_logging_type -
        #   enum [CONSOLE/FILE] None if out of bounds or not found
        try:
            self.library_logging_type: int = LogOutputType[
                configuration['library_logging_type']].value
        except KeyError:
            self.library_log_level: int = None


# Configuration holders
_app_configuration: Config = None
_default_configuration: Config = None


def get_default_config() -> Config:
    """
    Returns app default configuration. Raises RuntimeError if config is None

    Raises:
        RuntimeError: Raised if the config is None

    Returns:
        Config: Instance of Config class with default configuration
    """

    if _default_configuration is not None:
        return _default_configuration

    raise RuntimeError('Default config was None')


def get_config() -> Config:
    """
    Returns app configuration. Raises RuntimeError if config is None

    Raises:
        RuntimeError: Raised if config is None

    Returns:
        Config: Instance of Config class with default configuration
    """
    if _app_configuration is not None:
        return _app_configuration

    raise RuntimeError('App configuration was None')


def load_configuration() -> None:
    """
    Loads app configuration and default configuration to global variables and checks them
    """

    # Loading to dict from JSONs
    default_conf_dict: dict = _load_default_config()
    normal_conf_dict: dict = _load_config()

    # Initialization of instances
    default_config: Config = Config(default_conf_dict)
    app_config: Config = Config(normal_conf_dict)

    # Check default config
    for key, value in default_config.__dict__.items():
        try:
            assert value is not None
        except AssertionError as exc:
            raise InvalidConfigurationValue(key, _DEFAULT_CONFIG_PATH) from exc

    # Check user-defined configuration
    for key, value in app_config.__dict__.items():
        try:
            assert value is not None
        except AssertionError as exc:
            default_entry = getattr(default_config, key)
            print(
                'Config entry {} is missing or invalid, changing to default value {}'.format(
                    key, default_entry
                )
            )
            setattr(app_config, key, default_entry)

    # Bind configuration to globals
    globals()['_app_configuration'] = app_config
    globals()['_default_configuration'] = default_config


def _load_config() -> dict:
    """
    Loads app configuration from 'config.json' file and returns it as a python dictionary
    if the file is not found then it is created from a default config file. Raises error when
    json parser couldn't parse the file

    Raises:
        JsonDecodeError: Raised when JSON parser couldn't parse the file

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


class InvalidConfigurationValue(Exception):
    """
    Raised when app is configured with invalid config entry

    """

    def __init__(self, cause: str, context: str):
        message = f'Given value for configuration entry {cause} was invalid in {context}'
        super().__init__(message)


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
    Enum that represents different methods of writing log messages either to stdout in console
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
