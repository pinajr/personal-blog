from pwdlib import PasswordHash
import secrets
import hashlib

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def digest_session_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()