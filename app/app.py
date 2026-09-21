from flask import Flask, Response, jsonify, request, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)
REQUESTS = Counter("demo_http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
LATENCY = Histogram("demo_http_request_duration_seconds", "Request latency", ["endpoint"])

@app.before_request
def before():
    g.started = time.perf_counter()

@app.after_request
def after(response):
    elapsed = time.perf_counter() - getattr(g, "started", time.perf_counter())
    REQUESTS.labels(request.method, request.path, str(response.status_code)).inc()
    LATENCY.labels(request.path).observe(elapsed)
    return response

@app.get("/")
def home():
    app.logger.info("Home endpoint called")
    return jsonify(service="observability-demo", status="running")

@app.get("/health")
def health():
    return jsonify(status="healthy")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
