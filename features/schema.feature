Feature: Publish and get schema

  Scenario: Publish schema version 1
    Given there are no schemas in the database with the Survey ID test_survey_id
    When I call the Post Schema endpoint to publish version 1 schema with the Survey ID test_survey_id
    Then I should get the metadata of the schema with the Survey ID test_survey_id and version 1

  Scenario: Publish schema version 2
    Given there is 1 version of schema in the database with the Survey ID test_survey_id
    When I call the Post Schema endpoint to publish version 2 schema with the Survey ID test_survey_id
    Then I should get the metadata of the schema with the Survey ID test_survey_id and version 2

  Scenario: Get schema version 1
    Given there are 2 versions of schema in the database with the Survey ID test_survey_id
    When I call the Get Schema endpoint with Survey ID test_survey_id and version 1
    Then I should get the schema of version 1 of Survey ID test_survey_id

  Scenario: Get latest version of schema
    Given there are 2 versions of schema in the database with the Survey ID test_survey_id
    When I call the Get Schema endpoint with Survey ID test_survey_id and omit the version
    Then I should get the schema of version 2 of Survey ID test_survey_id
    