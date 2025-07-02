FROM python:3.11

WORKDIR /app

# Install system dependencies for torch/transformers
RUN apt-get update && \
    apt-get install -y --no-install-recommends git gcc libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# (Optional, but recommended for cold start in CI/prod):
# Pre-download models; comment out if you prefer to lazy-load
# RUN python -c "from transformers import pipeline; pipeline('translation', model='Helsinki-NLP/opus-mt-de-en'); pipeline('text-generation', model='t-systems-onsite/germangpt2-345M')"

# The Hugging Face cache is at /root/.cache/huggingface by default
# It is persisted via docker-compose (see: volumes: - hf_cache:/root/.cache/huggingface)

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
