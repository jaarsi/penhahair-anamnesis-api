# pylint: disable=bare-except

import os
from requests_oauthlib import OAuth2Session

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URI = os.getenv("GOOGLE_AUTH_URI")
GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI")
GOOGLE_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

def __google_oauth(**kwargs):
    return OAuth2Session(
        GOOGLE_CLIENT_ID,
        scope=GOOGLE_SCOPES,
        **kwargs
    )

def google_authorization(**kwargs):
    return __google_oauth(**kwargs).authorization_url(
        GOOGLE_AUTH_URI, access_type="offline", prompt="select_account"
    )

def google_token(authorization_response, **kwargs) -> dict:
    return __google_oauth(**kwargs).fetch_token(
        GOOGLE_TOKEN_URI,
        authorization_response=authorization_response,
        client_secret=GOOGLE_CLIENT_SECRET,
    )

def google_userinfo(**kwargs):
    try:
        response = __google_oauth(**kwargs).get("https://www.googleapis.com/oauth2/v1/userinfo")
    except:
        return None

    if response.status_code != 200:
        return None

    return response.json()
