FROM python:3.9-slim-buster AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /install /usr/local

COPY src /app/src

ENV PYTHONPATH=/app/src

ENV PROJECT_NAME="CloudWatch API Test"
ENV SERVICE_NAME="cw-api"
ENV LOG_LEVEL="INFO"
ENV API_PORT=80

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "src.main:app"]
