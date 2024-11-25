Feature: Publish and get dataset
  
  Scenario: Publish 3 datasets
    Given there are no datasets in the database with a set of test data
      | survey_id | period_id |
      | test_survey_id | 123 |
      | test_survey_id | 456 |
    When I publish a set of datasets
      | filename |
      | dataset_test_survey_id_123_v1.json |
      | dataset_test_survey_id_123_v2.json |
      | dataset_test_survey_id_456_v1.json |
    And I call the Get Dataset Metadata endpoint with the Survey ID test_survey_id and Period ID 123
    Then I should get 2 metadata of the dataset with the Survey ID test_survey_id and Period ID 123
      | filename | survey_id | period_id | title | total_reporting_units | sds_dataset_version |
      | dataset_test_survey_id_123_v2.json | test_survey_id | 123 | Dataset version 2 of test_survey_id and period_id 123 | 3 | 2 | 
      | dataset_test_survey_id_123_v1.json | test_survey_id | 123 | Dataset version 1 of test_survey_id and period_id 123 | 2 | 1 | 