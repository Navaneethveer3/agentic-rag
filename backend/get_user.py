from typing import Optional
from fastapi import Header
import os

def get_current_user(
    authorization: Optional[str] = Header(None),
    x_username: Optional[str] = Header(None),
) -> str:
    """
    Extracts the authenticated user's email/username.
    - If Authorization Bearer token is provided: decodes claims (Entra ID).
    - If X-Username header is passed: used for direct development/testing.
    """
    if x_username:
        return x_username.strip()

    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            # Decode JWT claims without verification for claim extraction (or use jwt/msal for full validation)
            import jwt
            decoded = jwt.decode(token, options={"verify_signature": False})
            username = decoded.get("preferred_username") or decoded.get("upn") or decoded.get("sub")
            if username:
                return username
        except Exception:
            pass

    # Default fallback for local testing if no header is supplied
    return os.getenv("DEFAULT_USER", "default_user")