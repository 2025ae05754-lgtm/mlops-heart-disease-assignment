# Stage 1: Dependency Assembly
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production Execution Runtime
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy source code and model artifacts
COPY src/ ./src/
COPY app/ ./app/
COPY models/ ./models/

EXPOSE 8000

USER 10001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]