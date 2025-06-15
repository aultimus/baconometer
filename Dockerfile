FROM python:3.10-slim

WORKDIR /app

COPY src/requirements.txt ./src/requirements.txt
RUN pip install --no-cache-dir -r src/requirements.txt

COPY src/ ./src/

# Default command (can be overridden by docker-compose)
CMD ["flask", "run", "--host=0.0.0.0"]
