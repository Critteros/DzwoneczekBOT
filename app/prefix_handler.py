

# Library includes
from firebase_admin import firestore


# App includes
from app.logging.core import Log

# Just for typing info
from google.cloud.firestore import Client as FirestoreClient
from google.cloud.firestore import DocumentReference


# Storage for prefixes
server_prefixes = {}


def get_server_prefix(guild_id: int) -> str:
    """
    Retrives sever prefix for given guild-id from firestore and caches it

    Returns:
        str: server prefix
    """
    # If prefix is arleady cached
    if guild_id in server_prefixes:
        Log.debug(f'Using cached prefix for server {guild_id}')
        return server_prefixes[guild_id]

    #################################

    Log.debug('Retriving prefix from firestore')
    # Retrive firestore client
    db_client: FirestoreClient = firestore.client()

    # Path to the document holding server configuration
    path_to_server_config: str = f'bot-root/{guild_id}/server-specific/server-config'

    # Get document reference
    doc_reference: DocumentReference = db_client.document(
        path_to_server_config)

    # Retrive server configuration
    server_configuration: dict = doc_reference.get().to_dict()

    # Check if server configuration exists
    if server_configuration is None:
        Log.debug(
            f'Firestore entry does noe exist for guild {guild_id}, creating entry')
        server_prefixes[guild_id] = ''
        doc_reference.set({'prefix': ''})  # Sets document with
        return ''

    prefix = server_configuration.get('prefix', '')
    server_prefixes[guild_id] = prefix
    return prefix
