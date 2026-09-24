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

## Running locally (backend)

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