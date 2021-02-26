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

    # Setup Loggers from config
    Log.config_init()
    Log.info('Logging is now available')

    # Get the configuration
    bot_configuration: configuration.Config = configuration.get_config()

    # Listing configuration
    Log.warning('Listing bot configuration:')

    for key, value in bot_configuration.__dict__.items():
        Log.warning(f'\t{key}: {value}')


if __name__ != '__main__':
    print('Bad entry point was used, use startup.py instead')
else:
    main()
