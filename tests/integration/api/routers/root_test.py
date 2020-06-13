import pytest


@pytest.mark.integration
def test_health_check(test_client, env_settings):
    with test_client:
        response = test_client.get("/status")
        assert response.status_code == 200
        assert response.json() == {
            "title": env_settings.WEB_APP_TITLE,
            "description": env_settings.WEB_APP_DESCRIPTION,
            "version": env_settings.WEB_APP_VERSION,
            "status": "OK",
        }
