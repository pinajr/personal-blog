# Personal Blog

> Work in progress — built as a full-stack learning project and
> portfolio piece for software development internship applications.

A full-stack personal blog with a FastAPI backend and a React
frontend (coming soon). Article CRUD, authentication, and
authorization are being developed progressively.

## Stack

- **Backend:** Python, FastAPI, Pydantic
- **Database:** PostgreSQL, SQLAlchemy *(coming soon)*
- **Frontend:** React, TypeScript, TailwindCSS, Vite *(coming soon)*

## Current status

- [x] Initial backend setup with FastAPI
- [x] Article CRUD (in-memory, no persistence yet)
- [ ] PostgreSQL
- [ ] Authentication and authorization
- [ ] Frontend
- [ ] Testing
- [ ] Docker
- [ ] Deployment

## Running locally

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- [Homebrew](https://brew.sh) (macOS)

### 1. Database

Install and start PostgreSQL via Homebrew:

```bash
brew install postgresql@18
echo 'export PATH="/opt/homebrew/opt/postgresql@18/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
brew services start postgresql@18
```

Create the project's database:

```bash
psql postgres
```
```sql
CREATE DATABASE personal_blog;
```

Exit with `\q`.

### 2. Backend

```bash
cd backend
uv sync
uv run fastapi dev main.py
```

Visit `http://localhost:8000/docs` for the interactive API
documentation.

## License

This project is licensed under the MIT License — see the
[LICENSE](LICENSE) file for details.