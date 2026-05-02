# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only application source — no .env or local data files
COPY src/ ./src/

# Create writable directories for runtime caches
# - .cache/ : cleaned parquet cache written by the pipeline
# - /tmp/hf_cache : HuggingFace datasets download cache (writable on Render free tier)
RUN mkdir -p .cache /tmp/hf_cache

# Environment configuration
ENV PYTHONPATH=.
ENV PORT=8000
ENV HF_HOME=/tmp/hf_cache
ENV TRANSFORMERS_CACHE=/tmp/hf_cache

# Expose the port Render will route to
EXPOSE 8000

# Start the FastAPI server (production-grade, no --reload)
CMD ["uvicorn", "src.milestone_1.main:app", "--host", "0.0.0.0", "--port", "8000"]
