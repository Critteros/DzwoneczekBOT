"""
This module handles complications of dynamic retrieving prefixes for diffrent servers
It requests server prefix from database and caches it for optimization

"""

# Library includes
from firebase_admin import firestore


# Library imports for typing hints
from google.cloud.firestore import Client as FirestoreClient
from google.cloud.firestore import DocumentReference

# App includes
from app.logging.core import Log


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

    Log.debug(f'Retriving prefix from firestore for server {guild_id}')
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


def set_server_prefix(guild_id: int, prefix: str) -> None:
    """
    Updates server prefix

    Args:
        guild_id (int): guild id
        prefix (str): prefix to be set
    """
    Log.info(f'Updating server({guild_id}) prefix to {prefix}')

    # Retrive Firestore Client
    db_client: FirestoreClient = firestore.client()

    # Path to server config
    path_to_server_config: str = f'bot-root/{guild_id}/server-specific/server-config'

    # Update cached prefix
    server_prefixes[guild_id] = prefix

    # Retrive document pointer
    doc_ref: DocumentReference = db_client.document(path_to_server_config)

    # Update value
    doc_ref.set({'prefix': prefix}, merge=True)
