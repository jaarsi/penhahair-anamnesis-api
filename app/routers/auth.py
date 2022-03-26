# pylint: disable=bare-except

import os
from functools import wraps
from urllib.parse import urljoin
from requests_oauthlib import OAuth2Session
from flask import Blueprint, request, redirect, session, url_for, jsonify

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URI = os.getenv("GOOGLE_AUTH_URI")
GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI")
GOOGLE_SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

class GoogleOAuth2:
    @classmethod
    def oauth2_session(cls, **kwargs):
        return OAuth2Session(GOOGLE_CLIENT_ID, scope=GOOGLE_SCOPES, **kwargs)

    @classmethod
    def authorization(cls, **kwargs):
        return cls.oauth2_session(**kwargs).authorization_url(
            GOOGLE_AUTH_URI,
            access_type="offline",
            prompt="select_account"
        )

    @classmethod
    def token(cls, authorization_response, **kwargs) -> dict:
        return cls.oauth2_session(**kwargs).fetch_token(
            GOOGLE_TOKEN_URI,
            authorization_response=authorization_response,
            client_secret=GOOGLE_CLIENT_SECRET,
        )

    @classmethod
    def userinfo(cls, **kwargs):
        try:
            response = cls.oauth2_session(**kwargs).get(
                "https://www.googleapis.com/oauth2/v1/userinfo"
            )
        except:
            return None

        if response.status_code != 200:
            return None

        return response.json()

def authentication_required(f):
    # pylint: disable=invalid-name
    @wraps(f)
    def g(*args, **kwargs):
        state, token = session.get("state", None), session.get("token", None)

        if not (current_user := GoogleOAuth2.userinfo(token=token, state=state)):
            session["current_user"] = current_user
            session["next"] = request.endpoint
            return redirect(url_for("auth.authentication_route"))

        return f(*args, **kwargs)

    return g

router = Blueprint("auth", __name__)

@router.get("/")
def authentication_route():
    state, token = session.get("state", None), session.get("token", None)
    redirect_uri = urljoin(request.host_url, url_for("auth.authentication_callback_route"))
    authorization_url, state = GoogleOAuth2.authorization(
        token=token,
        state=state,
        redirect_uri=redirect_uri,
    )
    session["state"] = state
    return redirect(authorization_url)

@router.get("/callback")
def authentication_callback_route():
    state, token = session.get("state", None), session.get("token", None)
    redirect_uri = urljoin(request.host_url, url_for("auth.authentication_callback_route"))
    token = GoogleOAuth2.token(request.url, token=token, state=state, redirect_uri=redirect_uri)
    session["token"] = token
    session["current_user"] = GoogleOAuth2.userinfo(token=token, state=state)

    if target_url := session.get("next", None):
        session["next"] = None
        return redirect(url_for(target_url))

    return redirect(url_for("auth.me_route"))

@router.get("/me")
@authentication_required
def me_route():
    return jsonify(current_user=session.get("current_user", None))
