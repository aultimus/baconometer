FROM python:3.10-slim

WORKDIR /app

COPY src/requirements.txt ./src/requirements.txt
RUN pip install --no-cache-dir -r src/requirements.txt

COPY src/ ./src/
COPY --chown=1000:1000 . .

# Expose port
EXPOSE 8000

# Use Gunicorn for production
# Default command (can be overridden by docker-compose)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "src.app:app"]
