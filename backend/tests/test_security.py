from app.core.security import create_access_token
from jose import jwt
from app.core.config import settings

def test_jwt_tampering_fails():
    token = create_access_token(subject=100)
    tampered = token[:-5] + "aaaaa"
    with pytest.raises(Exception):
        jwt.decode(tampered, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
