# ---- Build stage ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Runtime stage (small, no build tools) ----
FROM python:3.12-slim
WORKDIR /app

# Run as non-root (security best practice, required by most PodSecurity policies)
RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /install /usr/local
COPY app/ .

USER app
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "2", "main:app"]
