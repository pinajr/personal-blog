# Personal Blog

A full-stack personal blog built as a learning project and portfolio piece.

**Live site:** [pinajr.github.io/personal-blog](https://pinajr.github.io/personal-blog/)

The frontend is hosted on GitHub Pages. The FastAPI backend runs on Render and uses PostgreSQL hosted by Neon.

## Tech stack

- **Backend:** Python 3.12+, FastAPI, Pydantic, SQLAlchemy, Alembic
- **Database:** PostgreSQL (Neon in production)
- **Authentication:** Argon2 password hashing and database-backed session cookies
- **Backend tests:** pytest
- **Frontend:** React, TypeScript, Tailwind CSS, Vite, React Router
- **Local services:** Docker and Docker Compose
- **Deployment:** GitHub Actions and GitHub Pages (frontend), Render (backend), Neon (database)

## Project status

- [x] PostgreSQL persistence and Alembic migrations
- [x] Public article listing and detail endpoints
- [x] Article creation, update, and deletion
- [x] Login and logout with session-based authentication
- [x] Authorization: only the article owner can update or delete it
- [x] Command-line script to create the initial user; there is no public registration endpoint
- [x] Automated backend tests
- [ ] Automated frontend tests
- [x] Browser security hardening, including CORS and CSRF protection
- [x] Docker and Docker Compose for local development
- [x] Production deployment

## Run the full stack locally with Docker Compose

### Prerequisites

- Docker Desktop
- Git

### 1. Configure PostgreSQL

In the `.env` file in the repository root, make sure these local PostgreSQL settings are present. If the file already contains other settings, keep them and add or update only these three:

```dotenv
POSTGRES_DB=personal_blog
POSTGRES_USER=personal_blog
POSTGRES_PASSWORD=change-this-local-password
```

Keep `.env` private; it is ignored by Git. These values are for the local Compose database.

### 2. Start the services

From the repository root, build and start PostgreSQL, the backend, and the frontend:

```bash
docker compose up --build -d
```

### 3. Apply database migrations

```bash
docker compose exec backend uv run alembic upgrade head
```

### 4. Create the blog owner account

There is no public registration endpoint. Create the account used to manage articles:

```bash
docker compose exec backend uv run python create_admin.py
```

The command asks for a username, email, and password. It stores a password hash in the database.

### 5. Open the app

- Blog: [http://localhost:5173](http://localhost:5173)
- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

Stop the services with `docker compose down`. This keeps the local PostgreSQL volume and its data.

## Run the backend tests

From the `backend` directory, install the dependencies and run the tests:

```bash
uv sync
uv run pytest -q
```

The tests use a separate test database setup and do not require the production Neon database.

## Production configuration

- GitHub Actions builds the frontend and publishes it to GitHub Pages when changes are pushed to `main`.
- The frontend build uses the GitHub Actions variable `VITE_API_URL` to find the backend API.
- The Render backend uses environment variables for its Neon connection and allowed frontend origin. Do not commit database URLs, passwords, or other secrets.
- The Neon production database is separate from the local PostgreSQL database used by Docker Compose.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
