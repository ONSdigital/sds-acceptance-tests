# sds-acceptance-tests

```
export PROJECT_ID=$(gcloud config get project)
export OAUTH_BRAND_NAME=$(gcloud iap oauth-brands list --format='value(name)' --limit=1 --project=$(echo $PROJECT_ID))
export OAUTH_CLIENT_NAME=$(gcloud iap oauth-clients list $(echo $OAUTH_BRAND_NAME) --format='value(name)' \
        --limit=1)
export OAUTH_CLIENT_ID=$(echo $(echo $OAUTH_CLIENT_NAME)| cut -d'/' -f 6)
export SANDBOX_IP_ADDRESS=$(gcloud compute addresses list --global  --filter=name:$(echo $PROJECT_ID)-sds-static-lb-ip --format='value(address)' --limit=1 --project=$(echo $PROJECT_ID))
gcloud run jobs deploy acceptance-tests-run \
--source . \
--tasks 1 \
--set-env-vars PROJECT_ID=$(echo $PROJECT_ID) \
--set-env-vars FIRESTORE_DB_NAME=$(echo $PROJECT_ID)-sds \
--set-env-vars API_URL=https://$(echo $SANDBOX_IP_ADDRESS).nip.io \
--set-env-vars OAUTH_CLIENT_ID=$(echo $OAUTH_CLIENT_ID) \
--set-env-vars TEST_FAIL_FLAG=False \
--max-retries 0 \
--region europe-west2 \
--project=$(echo $PROJECT_ID)
```
