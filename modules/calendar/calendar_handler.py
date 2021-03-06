

# Library includes
import random

from firebase_admin import firestore

# Typing info
from google.cloud.firestore import Client as FirestoreClient

# App includes
from app.logging.core import Log


def load_guild_latest(guild_id: int):

    # Path to reference to callendar-events collection
    events_ref_string = f'bot-root/{guild_id}/calendar-events'

    # Firestore client
    db_client: FirestoreClient = firestore.client()

    # Collection holding the callendar events
    events_ref = db_client.collection(events_ref_string)

    # Retriving and sorting all callendar events
    query = events_ref.order_by(
        u'time', direction='ASCENDING').stream()

    for doc in query:
        Log.warning(f'{doc.id} => {doc.to_dict()}')


def next_uid(guild_id: int):

    Log.debug(f'Genereting new uid for callendar event in guild {guild_id}')
    # Initialize random seed
    random.seed()

    # Random number from 1000 to 9999 inclusive
    rand_number: int = random.randrange(1000, 10000)

    # The following part checks if the random id is unique
    db_client: FirestoreClient = firestore.client()  # The firestore client
    # String path to events
    path_to_events: str = f'bot-root/{guild_id}/calendar-events'
    coll_ref = db_client.collection(path_to_events)  # Collection reference

    Log.debug('Accesing firestore to verify uid')
    query = coll_ref.where(u'id', u'==', rand_number).get()

    # If it's unique already
    if not query:
        Log.debug(f'Generated {rand_number}')
        return rand_number
    else:
        return next_uid(guild_id)
