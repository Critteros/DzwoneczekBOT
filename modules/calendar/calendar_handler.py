

# Library includes

from firebase_admin import firestore

# Typing info
from google.cloud.firestore import Client as FirestoreClient

# App includes
from app.logging.core import Log


def load_guild_latest(guild_id: int):
    events_ref_string = f'bot-root/{guild_id}/calendar-events'
    Log.warning('called')

    db_client: FirestoreClient = firestore.client()

    events_ref = db_client.collection(events_ref_string)

    query = events_ref.order_by(
        u'time', direction='ASCENDING').stream()

    for doc in query:
        Log.warning(f'{doc.id} => {doc.to_dict()}')
