from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import requests
from app.config import (
    KEYCLOAK_URL_INTERNAL,
    KEYCLOAK_URL_PUBLIC,
    KEYCLOAK_REALM,
    KEYCLOAK_CLIENT_ID,
)

OIDC_CONFIG = f"{KEYCLOAK_URL_INTERNAL}/realms/{KEYCLOAK_REALM}/.well-known/openid-configuration"
JWKS_URL = ""
ALGORITHMS = ["RS256"]
TOKEN_URL = f"{KEYCLOAK_URL_PUBLIC}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
ISSUER = f"{KEYCLOAK_URL_PUBLIC}/realms/{KEYCLOAK_REALM}"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

def get_jwks_url():
    global JWKS_URL
    if not JWKS_URL:
        resp = requests.get(OIDC_CONFIG)
        resp.raise_for_status()
        JWKS_URL = resp.json()["jwks_uri"]
    return JWKS_URL

def get_public_key():
    jwks_url = get_jwks_url()
    resp = requests.get(jwks_url)
    resp.raise_for_status()
    return resp.json()

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    try:
        jwks = get_public_key()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "alg": key["alg"],
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
                break  # Stop once the right key is found

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Public key not found in JWKS."
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=KEYCLOAK_CLIENT_ID,  # Verify audience against your client id
            issuer=ISSUER,
            options={"verify_aud": True}  # Enable audience verification for security
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"JWT validation failed: {str(e)}"
        )
