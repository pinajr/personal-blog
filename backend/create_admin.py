from getpass import getpass
from pydantic import ValidationError

from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from models import User
from schemas import UserCreate
from security import get_password_hash


def main() -> None:
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    password_confirmation = getpass("Confirm password: ")

    if password != password_confirmation:
        print("Passwords do not match.")
        raise SystemExit(1)

    try:
        user = UserCreate(username=username, email=email, password=password)
    except ValidationError as e:
        print(e.errors(include_input=False))
        raise SystemExit(1)

    password_hash = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=password_hash)

    with SessionLocal() as db:
        db.add(new_user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            print("Username or email already exists.")
            raise SystemExit(1)

    print("User created successfully.")


if __name__ == "__main__":
    main()