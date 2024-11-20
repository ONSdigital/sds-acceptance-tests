import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import json

from behave import given, when, then, fixture
from behave.runner import Context
from config import config

@given("there are no schemas in the database with the Survey ID test_survey_id")
def step_impl(context: Context):
    response = context.api_client.get(
        f"{context.api_url}/v1/schema?survey_id=test_survey_id",
        headers=context.headers,
    )
    assert response.status_code == 404


@given("there is 1 version of schema in the database with the Survey ID test_survey_id")
def step_impl(context: Context):
    response = context.api_client.get(
        f"{context.api_url}/v1/schema_metadata?survey_id=test_survey_id",
        headers=context.headers,
    )
    assert response.status_code == 200
    schema_metadata = response.json()
    assert len(schema_metadata) == 1


@given("there are 2 versions of schema in the database with the Survey ID test_survey_id")
def step_impl(context: Context):
    response = context.api_client.get(
        f"{context.api_url}/v1/schema_metadata?survey_id=test_survey_id",
        headers=context.headers,
    )
    assert response.status_code == 200
    schema_metadata = response.json()
    assert len(schema_metadata) == 2


@when("I publish version 1 schema with the Survey ID test_survey_id")
def step_impl(context: Context):
    schema_json = json.load(open("test_data/json/schema_v1.json"))
    response = context.api_client.post(
        f"{context.api_url}/v1/schema?survey_id=test_survey_id",
        json=schema_json,
        headers=context.headers,
    )
    assert response.status_code == 200
    context.response_json = response.json()


@when("I publish version 2 schema with the Survey ID test_survey_id")
def step_impl(context: Context):
    schema_json = json.load(open("test_data/json/schema_v2.json"))
    response = context.api_client.post(
        f"{context.api_url}/v1/schema?survey_id=test_survey_id",
        json=schema_json,
        headers=context.headers,
    )
    assert response.status_code == 200
    context.response_json = response.json()
    

@when("I call the Get Schema endpoint with Survey ID test_survey_id and version 1")
def step_impl(context: Context):
    response = context.api_client.get(
        f"{context.api_url}/v1/schema?survey_id=test_survey_id&version=1",
        headers=context.headers,
    )

    assert response.status_code == 200
    context.response_json = response.json()


@when("I call the Get Schema endpoint with Survey ID test_survey_id and omit the version")
def step_impl(context: Context):
    response = context.api_client.get(
        f"{context.api_url}/v1/schema?survey_id=test_survey_id",
        headers=context.headers,
    )

    assert response.status_code == 200
    context.response_json = response.json()


@then("I should get the metadata of the schema with the Survey ID test_survey_id and version 1")
def step_impl(context: Context):
    guid = context.response_json["guid"]
    assert context.response_json == {
        "guid": guid,
        "schema_location": f"test_survey_id/{guid}.json",
        "sds_published_at": context.response_json["sds_published_at"],
        "sds_schema_version": 1,
        "survey_id": "test_survey_id",
        "schema_version": "v1",
        "title": "Schema version 1 of test_survey_id",
    }


@then("I should get the metadata of the schema with the Survey ID test_survey_id and version 2")
def step_impl(context: Context):
    guid = context.response_json["guid"]
    assert context.response_json == {
        "guid": guid,
        "schema_location": f"test_survey_id/{guid}.json",
        "sds_published_at": context.response_json["sds_published_at"],
        "sds_schema_version": 2,
        "survey_id": "test_survey_id",
        "schema_version": "v2",
        "title": "Schema version 2 of test_survey_id",
    }


@then("I should get the schema of version 1 of Survey ID test_survey_id")
def step_impl(context: Context):
    schema = context.response_json
    assert schema["title"] == "Schema version 1 of test_survey_id"
    assert schema["properties"]["schema_version"]["const"] == "v1"

    if config.TEST_FAIL_FLAG == "True":
        assert context.response_json == {"test": "fail"}


@then("I should get the schema of version 2 of Survey ID test_survey_id")
def step_impl(context: Context):
    schema = context.response_json
    assert schema["title"] == "Schema version 2 of test_survey_id"
    assert schema["properties"]["schema_version"]["const"] == "v2"

    if config.TEST_FAIL_FLAG == "True":
        assert context.response_json == {"test": "fail"}