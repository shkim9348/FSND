import json
import random
import string
from functools import wraps
from urllib.request import urlopen

from flask import current_app, g, request, session
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash

from pybo import db
from pybo.models import User


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization Header Missing",
            },
            401,
        )

    parts = auth_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            },
            401,
        )

    token = parts[1]
    return token


def check_permissions(permission, payload):
    # raise Exception("Not Implemented")

    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in JWT.",
            },
            400,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "Permission not found.",
            },
            403,
        )

    return True


def verify_decode_jwt(token):
    # it should be an Auth0 token with key id (kid)
    try:
        header = jwt.get_unverified_header(token)
    except JWTError:
        raise AuthError({"code": "invalid_header", "description": "You should Login first"}, 401)

    if "kid" not in header:
        raise AuthError({"code": "invalid_header", "description": "Token should contain kid"}, 401)

    # it should verify the token using Auth0 /.well-known/jwks.json
    iss = f"https://{current_app.config['AUTH0_DOMAIN']}/"
    res = urlopen(f"{iss}.well-known/jwks.json")
    jwks = json.loads(res.read())

    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == header["kid"]:
            rsa_key = key
            break

    if not rsa_key:
        raise AuthError(
            {"code": "invalid_header", "description": "Unable to find the appropriate key."}, 403
        )

    # it should decode the payload from the token
    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=current_app.config["AUTH0_ALGORITHMS"],
            audience=current_app.config['API_AUDIENCE'],
            issuer=f"https://{current_app.config['AUTH0_DOMAIN']}/",
        )

    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired", "description": "Token is expired"}, 401)

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
    if payload.get("iss") != iss:
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
            # authentication
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            # sso
            email = payload.get("email")
            email_verified = payload.get("email_verified")

            if g.user is None and email and email_verified:
                try:
                    user = db.session.execute(
                        db.select(User).filter_by(email=email),
                    ).scalar_one()
                except NoResultFound:
                    user = User(
                        username=email,
                        email=email,
                        # random password
                        password=generate_password_hash(
                            "".join(
                                random.choice(
                                    string.ascii_letters,
                                )
                                for i in range(8)
                            )
                        ),
                    )
                    db.session.add(user)
                    db.session.commit()

                # login
                session["user_id"] = user.id
                g.user = user

            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
