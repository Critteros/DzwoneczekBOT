"""
This file is the entrypoint of Bot application
"""

# Library includes


# App includes
import app.configuration as configuration
from app.logging.core import Log


def main() -> None:
    """
    Main function of bot application
    """

    # Load bot configuration from jsons
    configuration.load_configuration()

    Log.config_init()
    Log.debug('Example Debug')
    Log.info('Example info')
    Log.warning('Example warning')
    Log.error('Example error')
    Log.critical('Example critical')

    quick_logger = Log.get_exclusive_console(name='test')
    quick_logger.critical('test')


if __name__ != '__main__':
    print('Bad entry point was used, use startup.py instead')
else:
    main()
