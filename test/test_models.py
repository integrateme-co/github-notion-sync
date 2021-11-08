import pytest
from mixer.backend.django import mixer

@pytest.mark.django_db
class TestSaveAPIs:
    """Testing All Models"""
    def test_saving_dev(self):
        """Testing API Store Model"""
        apis = mixer.blend(
            'api_data.apiStoreModel',
            dev_api="TESTING_DEV_API",
            medium_api="TESTING_MEDIUM_API",
            hashnode_api="TESTING_HAHSH_API"
        )
        assert apis.dev_api == "TESTING_DEV_API"
        assert apis.hashnode_api == "TESTING_HAHSH_API"
        assert apis.medium_api == "TESTING_MEDIUM_API"

    def test_integration_model(self):
        """Testing Integration Model"""
        integration = mixer.blend(
            'api_data.integrationModel',
            user_id=99,
            notion_Oauth="DUMMY_NOTION_OAUTH",
            notion_pg_id="DUMMY_PAGE_ID",
            notion_db_id="DUMMY_DB_ID",
            sync_url="https://api.integrateme.co/testing"
        )
        assert integration.user_id == 99
        assert integration.notion_Oauth == "DUMMY_NOTION_OAUTH"
        assert integration.notion_pg_id == "DUMMY_PAGE_ID"
        assert integration.notion_db_id == "DUMMY_DB_ID"
        assert integration.sync_url == "https://api.integrateme.co/testing"
