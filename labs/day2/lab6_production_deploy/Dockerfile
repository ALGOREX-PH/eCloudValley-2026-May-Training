FROM python:3.12-slim

WORKDIR /app

# Install build tools required by some Python deps (e.g. chromadb's onnxruntime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (layer-cached when source changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole project so relative imports work the same as in dev
COPY . .

EXPOSE 8000

# Run the FastAPI app from the lab folder
CMD ["uvicorn", "labs.day2.lab6_production_deploy.starter:api", \
     "--host", "0.0.0.0", \
     "--port", "8000"]
