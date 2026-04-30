# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY .env .env
# Ensure cache dir exists for dataset
RUN mkdir -p .cache

# Copy dataset (or download on start if not present)
# Note: For production, you might want to fetch this from a CDN instead of baking into image
COPY .cache/zomato.csv .cache/zomato.csv

# Set environment variables
ENV PYTHONPATH=.

# Expose port
EXPOSE 8000

# Start server
CMD ["python", "-m", "src.milestone_1.main"]
