# Personal Blog

> A full-stack personal blog project built as a learning project and portfolio piece.

The backend is built with FastAPI and PostgreSQL. The frontend is planned with React, TypeScript, Tailwind CSS, and Vite.

## Tech stack

- **Backend:** Python 3.12+, FastAPI, Pydantic, SQLAlchemy, Alembic
- **Database:** PostgreSQL
- **Authentication:** Argon2 password hashing and database-backed session cookies
- **Backend tests:** pytest
- **Frontend:** React, TypeScript, Tailwind CSS, Vite *(planned)*

## Project status

- [x] PostgreSQL persistence and Alembic migrations
- [x] Public article listing and article detail endpoints
- [x] Article creation, update, and deletion
- [x] Login and logout with session-based authentication
- [x] Authorization: only the article owner can update or delete it
- [x] Automated backend tests
- [x] Command-line script to create the initial user; there is no public registration endpoint
- [ ] Frontend
- [ ] Browser security hardening, including CORS and CSRF protection
- [ ] Docker and Docker Compose
- [ ] Production deployment

## Run the backend locally

### Prerequisites

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL installed and running

### 1. Create a PostgreSQL database

Create a database named `personal_blog` using your PostgreSQL tools. For example, if your local PostgreSQL user has permission:

```bash
createdb personal_blog
```

### 2. Configure the database connection

From the repository root, move into the backend directory and set `DATABASE_URL` in your terminal. Replace `USER` and `PASSWORD` with your PostgreSQL credentials:

```bash
cd backend
export DATABASE_URL="postgresql+psycopg://USER:PASSWORD@localhost:5432/personal_blog"
```

Keep the value in your environment; do not commit credentials to the repository.

### 3. Install dependencies and apply migrations

```bash
uv sync
uv run alembic upgrade head
```

### 4. Create the initial user

There is no public registration endpoint. Create the blog owner account with the command-line script:

```bash
uv run python create_admin.py
```

The script asks for a username, email, and password, then stores a password hash in the database.

### 5. Start the API

```bash
uv run fastapi dev main.py
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) to explore the interactive API documentation.

## Run the backend tests

From the `backend` directory, with `uv` dependencies installed:

```bash
uv run pytest -q
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
