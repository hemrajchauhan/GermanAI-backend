FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if needed (none required for most FastAPI projects)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Expose FastAPI port (optional/documentation)
EXPOSE 8080

# Default env var for Ollama URL, can be overridden by Docker Compose or at runtime
ENV OLLAMA_URL=http://localhost:11434/api/generate

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]