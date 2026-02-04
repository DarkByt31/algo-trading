FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (including curl and mysql client)
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/stocks || exit 1

# Run entrypoint
ENTRYPOINT ["/entrypoint.sh"]
