import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import json

import google.oauth2.id_token
from google.cloud import firestore, storage
from behave.runner import Context
from config import config


def api_client():
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


def firestore_client():
    firestore_client = firestore.Client(project=config.PROJECT_ID, database=config.FIRESTORE_DB_NAME)

    return firestore_client


def storage_client():
    storage_client = storage.Client(project=config.PROJECT_ID)

    return storage_client


def get_bucket(bucket_name: str) -> storage.Bucket:
    """
    Method to get the bucket from the storage client.

    Parameters:
        storage_client (storage.Client): the storage client to use.
        bucket_name (str): the name of the bucket to get.

    Returns:
        storage.Bucket: the bucket to use.
    """
    client = storage_client()
    bucket = client.get_bucket(bucket_name)

    return bucket

    

def generate_headers() -> dict[str, str]:
    """
    Method to create headers for authentication if connecting to a remote version of the API.

    Parameters:
        None

    Returns:
        dict[str, str]: the headers required for remote authentication.
    """
    headers = {}

    auth_req = google.auth.transport.requests.Request()
    auth_token = google.oauth2.id_token.fetch_id_token(
        auth_req, audience=config.OAUTH_CLIENT_ID
    )

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    return headers


def cleanup_test_data():
    """
    Method to clean up the test data after each test.

    Parameters:
        None

    Returns:
        None
    """
    client = firestore_client()
    schema_collection = client.collection('schemas')

    perform_delete_on_collection_with_test_survey_id(
        client,
        schema_collection,
        "test_survey_id"
    )

    datsaet_collection = client.collection('datasets')

    perform_delete_on_collection_with_test_survey_id(
        client,
        datsaet_collection,
        "test_survey_id"
    )


def perform_delete_on_collection_with_test_survey_id(
    client: firestore.Client, collection_ref: firestore.CollectionReference, test_survey_id: str
) -> None:
    """
    Recursively deletes the collection and its subcollections.

    Parameters:
    collection_ref (firestore.CollectionReference): the reference of the collection being deleted.
    """

    # Query the collection for documents equivalent to survey_id LIKE "test_survey_id%"
    # \uf8ff is a unicode character that is greater than any other character
    doc_collection = (
        collection_ref.where('survey_id', '>=', test_survey_id)
        .where('survey_id', '<=', test_survey_id + '\uf8ff')
        .stream()
    )

    for doc in doc_collection:
        _delete_document(client, doc.reference)


def _delete_document(client: firestore.Client, doc_ref: firestore.DocumentReference) -> None:
    """
    Deletes the dataset with Document Reference

    Parameters:
    doc_ref (firestore.DocumentReference): The reference to the dataset to be deleted.
    """
    batch_size = 100

    for sub_collection in doc_ref.collections():
        
        while True:
            doc_deleted = _delete_sub_collection_in_batches(client, sub_collection, batch_size)
            if doc_deleted < batch_size:
                break

    doc_ref.delete()

    return True


def _delete_sub_collection_in_batches(
        client: firestore.Client,
        sub_collection_ref: firestore.CollectionReference,
        batch_size: int
    ) -> int:
    """
    Deletes a sub collection in batches.

    Parameters:
    sub_collection_ref (firestore.CollectionReference): The reference to the sub collection
    batch_size (int): The size of the batch to be deleted

    Returns:
    int: Number of documents deleted in the sub collection.
    """
    docs = sub_collection_ref.limit(batch_size).get()
    doc_count = 0

    batch = client.batch()

    for doc in docs:
        doc_count += 1
        batch.delete(doc.reference)                    

    batch.commit()

    return doc_count


# Run once before any features and scenarios are run
def before_all(context: Context):
    cleanup_test_data()

    context.api_client = api_client()
    context.api_url = config.API_URL
    context.headers = generate_headers()
    context.dataset_bucket = get_bucket(config.DATASET_BUCKET_NAME)
    context.publish_dataset_function_url = f"https://europe-west2-{config.PROJECT_ID}.cloudfunctions.net/new-dataset-function"


# Run once after all features and scenarios are run
def after_all(context: Context):
    cleanup_test_data()
    