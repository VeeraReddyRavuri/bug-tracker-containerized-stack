# -----Builder Stage -----

FROM python:3.11-alpine AS builder

WORKDIR /app

RUN apk add --no-cache build-base

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ----- Final Stage -----

FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app ./app

RUN adduser -D appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]