from operator import attrgetter

from todolist.config.environment import get_settings


oauth2_instrospect_url = "/account/oauth2/instrospect"
oauth2_token_url = "/account/oauth2/token"
secret_key = attrgetter("JWT_SECRET_KEY")(get_settings())


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def build_form_data(credentials):
    return {
        "grant_type": "password",
        "username": credentials.email,
        "password": credentials.password,
    }
