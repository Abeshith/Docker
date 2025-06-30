## Stage 1
FROM python:3.9 AS builder

WORKDIR /app

COPY calculator.py .

## Stage 2
FROM gcr.io/distroless/python3

WORKDIR /app

COPY --from=builder /app/calculator.py .

CMD ["calculator.py"]

