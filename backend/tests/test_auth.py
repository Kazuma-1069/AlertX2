import pytest
from app.core.security import verify_password, get_password_hash, create_access_token
from jose import jwt
from app.core.config import settings

def test_password_hashing():
    pwd = "EmergencySecurePass123!"
    hashed = get_password_hash(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("wrongpass", hashed) is False

def test_token_creation():
    user_id = 42
    token = create_access_token(subject=user_id)
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert int(payload["sub"]) == user_id
