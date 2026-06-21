FROM python:3.10-slim

WORKDIR /app

# rtree (required by osmnx) needs libspatialindex
RUN apt-get update && apt-get install -y --no-install-recommends \
    libspatialindex-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt huggingface_hub

COPY . .

# Download OSM graph + trained model from HuggingFace Hub at build time
ARG HF_REPO_ID
ENV HF_REPO_ID=${HF_REPO_ID}
RUN python scripts/download_assets.py

EXPOSE 9000

CMD ["sh", "-c", "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-9000}"]
