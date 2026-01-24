# Use small Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Chromium only (minimal)
RUN apt-get update && apt-get install -y \
    chromium \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies first (Docker layer caching)
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy backend code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]