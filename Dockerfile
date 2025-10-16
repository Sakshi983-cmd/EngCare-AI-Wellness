# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV STREAMLIT_SERVER_PORT=8501
ENV FASTAPI_PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to container
COPY . .

# Create necessary directories
RUN mkdir -p logs assets/css assets/js assets/images data

# Expose ports
EXPOSE 8501  # Streamlit
EXPOSE 8000  # FastAPI

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# Command to run both Streamlit and FastAPI
CMD ["sh", "-c", "streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & uvicorn backend.main:app --host 0.0.0.0 --port 8000"]
