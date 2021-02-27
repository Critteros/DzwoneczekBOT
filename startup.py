"""
This file is the entrypoint of Bot application
"""

# Library includes
import asyncio

import firebase_admin
from firebase_admin import credentials, firestore

# App includes
import app.configuration as configuration
from app.logging.core import Log
from app.client import BotClient

# Just for typing information
from google.cloud.firestore import Client as FirestoreClient


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

    Log.warning('Initializing firebase')
    cred = credentials.Certificate('.firebase')
    firebase_admin.initialize_app(credential=cred)

    # Just testing
    test_server_id = '792497879175397456'
    # db: FirestoreClient = firestore.client()
    # server_stuff = db.collection(f'bot-root/{test_server_id}/server-specific')

    # server_config = server_stuff.document('server-config').get().to_dict()

    # prefix = server_config.get('prefix')
    # Log.info(f'prefix is {prefix}')

    client = BotClient()
    asyncio.get_event_loop().run_until_complete(client.start())


if __name__ != '__main__':
    print('Bad entry point was used, use startup.py instead')
else:
    main()
