from config_helpers import get_value_from_env


class Config:
    PROJECT_ID = get_value_from_env("PROJECT_ID", "ons-cir-sandbox-384314")
    FIRESTORE_DB_NAME = get_value_from_env("FIRESTORE_DB_NAME", "ons-cir-sandbox-384314-sds")
    API_URL = get_value_from_env("API_URL", "")
    DATASET_BUCKET_NAME = get_value_from_env("DATASET_BUCKET_NAME", f"{PROJECT_ID}-sds-europe-west2-datasets")
    OAUTH_CLIENT_ID = get_value_from_env("OAUTH_CLIENT_ID", "")
    TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    TEST_FAIL_FLAG = get_value_from_env("TEST_FAIL_FLAG", "False")

config = Config()