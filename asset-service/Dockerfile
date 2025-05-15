FROM python:3.12-slim AS builder

WORKDIR /build
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

# Use Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]