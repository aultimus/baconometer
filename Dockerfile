FROM python:3.10-slim

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Install poetry for dependency management
ARG POETRY_VERSION=2.0.1
RUN pip install "poetry==${POETRY_VERSION}"
RUN poetry install --no-root --no-interaction

ENV PYTHONPATH="/app/src"


RUN poetry install --no-root

COPY src/ ./src/
COPY --chown=1000:1000 . .

# Expose port
EXPOSE 8000

# Use Gunicorn for production
# Default command (can be overridden by docker-compose)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "baconometer.wsgi:app"]
