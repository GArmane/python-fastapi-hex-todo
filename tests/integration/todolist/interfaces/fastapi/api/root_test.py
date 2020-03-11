import pytest


@pytest.mark.integration
def test_health_check(test_client, current_env_settings):
    response = test_client.get("/status")
    assert response.status_code == 200
    assert response.json() == {
        "title": current_env_settings.WEB_APP_TITLE,
        "description": current_env_settings.WEB_APP_DESCRIPTION,
        "version": current_env_settings.WEB_APP_VERSION,
        "status": "OK",
    }
