"""
This file is the entrypoint of Bot application
"""

# Library includes
import asyncio

import firebase_admin
from firebase_admin import credentials

# App includes
import app.configuration as configuration
from app.logging.core import Log
from app.client import BotClient


def main() -> None:
    """
    Main function of bot application
    """
    print('Starting up')

    # Setting up the configuration
    configuration.load_configuration()

    # Setup Loggers from config
    Log.config_init()
    Log.info('Logging is now available')

    # Retrive the app configuration
    bot_configuration: configuration.Config = configuration.get_config()

    # List the given configuration
    Log.warning('Listing bot configuration:')
    for key, value in bot_configuration.__dict__.items():
        Log.warning(f'\t{key}: {value}')
    Log.warning('End of configuration')

    # Setting up the firebase
    Log.warning('Initializing firebase connection')
    cred = credentials.Certificate('.firebase')
    firebase_admin.initialize_app(credential=cred)
    Log.warning('Firebase was initiatied successfully')

    # Creating bot instance
    Log.warning('Creating BotClient instance')
    client = BotClient()
    asyncio.get_event_loop().run_until_complete(client.start())


if __name__ != '__main__':
    print('Bad entry point was used, use startup.py instead')
else:
    main()
