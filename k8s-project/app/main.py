"""
Minimal demo web app for the K8s production project.
Exposes:
  GET /        -> basic hello page (reads config from env / ConfigMap)
  GET /health  -> liveness probe target
  GET /ready   -> readiness probe target
  GET /metrics -> Prometheus metrics endpoint
"""
import os
import time
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

APP_NAME = os.environ.get("APP_NAME", "k8s-demo-app")
APP_ENV = os.environ.get("APP_ENV", "development")
START_TIME = time.time()

REQUEST_COUNT = Counter("app_requests_total", "Total HTTP requests", ["endpoint"])


@app.route("/")
def index():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return jsonify(
        message=f"Hello from {APP_NAME}",
        environment=APP_ENV,
        uptime_seconds=round(time.time() - START_TIME, 2),
    )


@app.route("/health")
def health():
    # Liveness: is the process alive/responsive at all
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return jsonify(status="ok"), 200


@app.route("/ready")
def ready():
    # Readiness: is the app ready to serve traffic (e.g. DB connected)
    REQUEST_COUNT.labels(endpoint="/ready").inc()
    return jsonify(status="ready"), 200


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
