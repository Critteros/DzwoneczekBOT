"""
Core of the bot logging system. Contains functions that provides
logging capabilities through application
"""

# Library includes
import os
import logging
from sys import stdout

import coloredlogs


# App includes
import app.configuration as configuration

# Styles
logging_format: str = "%(asctime)s | %(name)s[%(process)d] %(levelname)s: %(message)s"

field_style: dict = {
    'asctime': {'color': 'white'},
    'hostname': {'color': 'magenta'},
    'levelname': {'bold': True, 'color': 'black'},

    'name': {'color': 214},
    'process': {'color': 90},
    'programname': {'color': 'cyan'},
    'username': {'color': 'yellow'}
}

level_style: dict = {
    'debug': {'color': 'black', 'bright': True},
    'info': {},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 16, 'background': 'red'},

    'notice': {'color': 'magenta'},
    'spam': {'color': 'green', 'faint': True},
    'success': {'bold': True, 'color': 'green'},
    'verbose': {'color': 'blue'}

}

datefmt: str = '%Y-%m-%d %H:%M:%S'


class Log:
    """
    Wrapper around logging and coloredlogs modules
    """
    # Container for active loggers
    active_loggers = []

    @staticmethod
    def config_init() -> None:
        """
        Initiaties loggers
        """
        # Get the app configuration
        config = configuration.get_config()

        # Setups Library Logger
        if config.log_library:

            # library_logginng_type
            # 1 means log to file
            # 0 means log to console
            if config.library_logging_type:
                logger_instance = _init_console(
                    name='discord',
                    level=config.library_log_level,
                    use_color=config.console_use_color
                )
                Log.active_loggers.append(logger_instance)
            else:
                logger_instance = _init_file(
                    name='discord',
                    level=config.library_log_level
                )
                Log.active_loggers.append(logger_instance)

        # Setups Console Logger
        if config.log_to_console:
            logger_instance = _init_console(
                name='BOT_CONSOLE',
                level=config.console_log_level,
                use_color=config.console_use_color
            )
            Log.active_loggers.append(logger_instance)

        # Setups File Logger
        if config.log_to_file:
            logger_instance = _init_file(
                name='BOT_FILE',
                level=config.file_log_level
            )
            Log.active_loggers.append(logger_instance)

    @staticmethod
    def get_exclusive_console(*, name, level=logging.INFO) -> logging.Logger:
        """
        Returns exclusive logger with formatting the same as in the main app.
        Independent of Log.info() debug etc. This logger will print to console
        Log does not record returned Log instance returned from this function

        Args:
            name (str): name of the logger
            level (int, optional): Logging level. Defaults to logging.INFO.

        Returns:
            logging.Logger: Logger instance
        """
        use_color: int = configuration.get_config().console_use_color
        return _init_console(name=name, level=level, use_color=use_color)

    @staticmethod
    def get_exclusive_file(*, name, level=logging.INFO) -> logging.Logger:
        """
        Returns exclusive logger with formatting the same as in the main app.
        Independent of Log.info() debug etc. This logger will print to file
        Log does not record returned Log instance returned from this function

        Args:
            name (str): Logger name
            level (int, optional): Logging level. Defaults to logging.INFO.

        Returns:
            logging.Logger: Logger instance
        """
        return _init_file(name=name, level=level)

    # Passthrough methods
    ######################################################################
    @staticmethod
    def debug(*args, **kwargs) -> None:
        """
        Prints debug message through all active loggers
        """
        # Assert that there are some active loggers
        assert Log.active_loggers

        for logger in Log.active_loggers:
            logger.debug(*args, **kwargs)

    @staticmethod
    def info(*args, **kwargs) -> None:
        """
        Prints info message through all active loggers
        """

        # Assert that there are some active loggers
        assert Log.active_loggers

        for logger in Log.active_loggers:
            logger.info(*args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs) -> None:
        """
        Prints warning message through all active loggers
        """

        # Assert that there are some active loggers
        assert Log.active_loggers

        for logger in Log.active_loggers:
            logger.warning(*args, **kwargs)

    @staticmethod
    def error(*args, **kwargs) -> None:
        """
        Prints error message through all active loggers
        """

        # Assert that there are some active loggers
        assert Log.active_loggers

        for logger in Log.active_loggers:
            logger.error(*args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs) -> None:
        """
        Prints critical message through all active loggers
        """
        # Assert that there are some active loggers
        assert Log.active_loggers

        for logger in Log.active_loggers:
            logger.critical(*args, **kwargs)


def _init_console(*, name: str, level: int, use_color: bool) -> None:

    # Retrive console logger
    logging_instance: logging.Logger = logging.getLogger(name)

    # Set logger level
    logging_instance.setLevel(level)

    if use_color:
        coloredlogs.install(
            level=level,
            fmt=logging_format,
            level_styles=level_style,
            field_styles=field_style,
            logger=logging_instance,
            stream=stdout
        )
    else:

        # Create Handler
        handler = logging.StreamHandler(stdout)
        handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(
            fmt=logging_format, datefmt=datefmt
        )

        handler.setFormatter(formatter)
        logging_instance.addHandler(handler)

    return logging_instance


def _init_file(*, name: str, level: int) -> None:
    """
    Activates and configures the file logger.
    For internal use only

    Args:
        level (int): Logging level
    """

    # Try to make a Logs directory if one does not exist
    try:
        os.mkdir('Logs')
    except OSError:
        pass

    logging_instance: logging.Logger = logging.getLogger(name)
    logging_instance.setLevel(level)

    file_name: str = name.lower() + '-log'

    # Handler
    handler = logging.FileHandler(f'Logs/{file_name}.log')
    handler.setLevel(level)

    # Formatter
    formatter: logging.Formatter = logging.Formatter(
        fmt=logging_format,
        datefmt=datefmt
    )

    handler.setFormatter(formatter)
    logging_instance.addHandler(handler)

    return logging_instance
