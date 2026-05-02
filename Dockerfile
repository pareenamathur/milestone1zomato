# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only application source — no .env or local data files
COPY src/ ./src/

# Ensure cache directory exists (dataset will be downloaded at runtime)
RUN mkdir -p .cache

# Set required environment variables (secrets provided at runtime via Render)
ENV PYTHONPATH=.
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Start the FastAPI server using uvicorn directly (production-grade)
CMD ["uvicorn", "src.milestone_1.main:app", "--host", "0.0.0.0", "--port", "8000"]
