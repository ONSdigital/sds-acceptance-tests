# Global Variables
GOOGLE_APPLICATION_CREDENTIALS=sandbox-key.json
PROJECT_ID = $(shell gcloud config get project)
OAUTH_BRAND_NAME = $(shell gcloud iap oauth-brands list --format='value(name)' --limit=1 --project=$(PROJECT_ID))
OAUTH_CLIENT_NAME = $(shell gcloud iap oauth-clients list $(OAUTH_BRAND_NAME) --format='value(name)' \
        --limit=1)
OAUTH_CLIENT_ID = $(shell echo $(OAUTH_CLIENT_NAME)| cut -d'/' -f 6)
SANDBOX_IP_ADDRESS = $(shell gcloud compute addresses list --global  --filter=name:$(PROJECT_ID)-sds-static-lb-ip --format='value(address)' --limit=1 --project=$(PROJECT_ID))

acceptance-test:
	export PROJECT_ID=$(PROJECT_ID) && \
	export FIRESTORE_DB_NAME=$(PROJECT_ID)-sds && \
	export API_URL=https://$(SANDBOX_IP_ADDRESS).nip.io && \
	export DATASET_BUCKET_NAME=${PROJECT_ID}-sds-europe-west2-dataset && \
	export OAUTH_CLIENT_ID=$(OAUTH_CLIENT_ID) && \
	export GOOGLE_APPLICATION_CREDENTIALS=$(GOOGLE_APPLICATION_CREDENTIALS) && \
	behave