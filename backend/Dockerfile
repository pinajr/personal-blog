# Build an image with the Python 3.12 image
FROM python:3.12-slim

# Set the working directory to `/app`
WORKDIR /app

# Copy `pyproject.toml` and `uv.lock`
COPY pyproject.toml uv.lock ./

# Install the Python dependencies
RUN pip install --no-cache-dir uv==0.12.18
RUN uv sync --locked --no-dev

# Copy the current directory `.` in the project to the workdir `.` in the image
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]