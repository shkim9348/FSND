import json
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from config import app_config

## AuthError Exception
"""
AuthError Exception
A standardized way to communicate auth failure modes
"""


auth = app_config["auth"]

AUTH0_DOMAIN = auth.AUTH0_DOMAIN
ALGORITHMS = auth.ALGORITHMS
API_AUDIENCE = auth.API_AUDIENCE


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    parts = auth_header.split()
    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 'Authorization header must start with "Bearer".',
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found."}, 401)
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token.",
            },
            401,
        )
    return parts[1]


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "RBAC not settings in Auth0 or Permissions not included in JWT.",
            },
            400,
        )

    print(payload)
    print(payload["permissions"])
    if permission not in payload["permissions"]:
        raise AuthError({"code": "unauthorized", "description": "Permission not found."}, 403)

    return True


def verify_decode_jwt(token):
    header = jwt.get_unverified_header(token)
    if "kid" not in header:
        raise AuthError({"code": "invalid_header", "description": "token should contain kid"}, 401)

    # it should verify the token using Auth0 /.well-known/jwks.json
    iss = f"https://{AUTH0_DOMAIN}/"
    res = urlopen(f"{iss}.well-known/jwks.json")
    jwks = json.loads(res.read())

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == header["kid"]:
            rsa_key = key
            break

    if not rsa_key:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Unable to find the appropriate key.",
            },
            403,
        )

    # it should decode the payload from the token
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )

    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired", "description": "token is expired"}, 401)

    except jwt.JWTClaimsError:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Incorrect claims, please check the audience and issuer",
            },
            401,
        )

    except Exception:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Unable to parse authentication token.",
            },
            401,
        )

    # it should validate the claims
    if payload.get("aud") != API_AUDIENCE or payload.get("iss") != iss:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Invalid claims",
            },
            401,
        )

    # return the decoded payload
    return payload


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
