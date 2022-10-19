import json
from functools import wraps

import inject
from flask import _request_ctx_stack
from flask_restx import abort
from flask_restx.reqparse import request as rq_flask
from requests import request

from jose import jwt

from src.infrastructure.adapters.flask.app.utils.error_handling import  api_error
from src.infrastructure.config.default_infra import AUTH0_DOMAIN, AUTH0_API_AUDIENCE, AUTH0_ALGORITHMS


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = rq_flask.headers.get("Authorization", None)
    if not auth:
        e = api_error('AuthorizationHeaderMissing')
        abort(code=e.status_code, message=e.message, error=e.error)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        e = api_error('InvalidHeaderByBearer')
        abort(code=e.status_code, message=e.message, error=e.error)

    elif len(parts) == 1:
        e = api_error('BearerTokenMissing')
        abort(code=e.status_code, message=e.message, error=e.error)

    elif len(parts) > 2:
        e = api_error('InvalidHeaderByShapeToken')
        abort(code=e.status_code, message=e.message, error=e.error)

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid
    """

    @wraps(f)
    @inject.autoparams('api_error')
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        jsonurl = request("GET", url, headers={}, data={})
        jwks = json.loads(jsonurl.content)
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=AUTH0_ALGORITHMS,
                    audience=AUTH0_API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/"
                )
            except jwt.ExpiredSignatureError:
                e = api_error('TokenExpiredError')
                abort(code=e.status_code, message=e.message, error=e.error)

            except jwt.JWTClaimsError:
                e = api_error('InvalidClimsError')
                abort(code=e.status_code, message=e.message, error=e.error)

            except Exception:
                e = api_error('InvalidHeaderUnknownError')
                abort(code=e.status_code, message=e.message, error=e.error)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)

        e = api_error('InvalidHeaderByKeyError')
        abort(code=e.status_code, message=e.message, error=e.error)

    return decorated
