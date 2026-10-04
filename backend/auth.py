from datetime import datetime, timezone

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from models import LoginSession, User
from security import digest_session_token


def get_current_user(
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_session),
) -> User:
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or expired session",
    )
    if not session_token:
        raise unauthorized

    token_hash = digest_session_token(session_token)
    current_time = datetime.now(timezone.utc)
    login_session = (
        db.query(LoginSession)
        .filter(
            LoginSession.token_hash == token_hash,
            LoginSession.expires_at > current_time,
        )
        .first()
    )
    if login_session is None:
        raise unauthorized

    user = db.query(User).filter(User.id == login_session.user_id).first()
    if user is None:
        raise unauthorized
    return user
