import time
import random
from flask import Flask, request, jsonify
from prometheus_client import (
        Counter, Gauge, Histogram, generate_latest
        )

app = Flask(__name__)

# ======================
# HTTP METRICS
# ======================
HTTP_REQUESTS = Counter(
        "lw_http_requests_total",
        "Total HTTP requests",
        ["method", "endpoint", "status"]
        )

HTTP_LATENCY = Histogram(
        "http_request_duration_seconds",
        "HTTP request latency",
        ["endpoint"]
        )

HTTP_ERRORS = Counter(
        "http_requests_errors_total",
        "Total HTTP errors",
        ["endpoint"]
        )

INFLIGHT = Gauge(
        "app_inflight_requests",
        "Requests currently being processed"
        )

# ======================
# BUSINESS METRICS
# ======================
ORDERS_CREATED = Counter(
        "orders_created_total",
        "Total orders created"
        )

APP_HEALTH = Gauge(
        "app_health_status",
        "App health (1 = healthy)"
        )

# ======================
# ROUTES
# ======================
@app.route("/order", methods=["POST"])
def create_order():
    start_time = time.time()
    INFLIGHT.inc()

    try:
        # simulate processing
        time.sleep(random.uniform(0.1, 0.8))

        # simulate random failure
        if random.random() < 0.2:
            HTTP_ERRORS.labels(endpoint="/order").inc()
            HTTP_REQUESTS.labels(
                    method="POST",
                    endpoint="/order",
                    status="500"
                    ).inc()
            return jsonify({"error": "order failed"}), 500

        ORDERS_CREATED.inc()
        HTTP_REQUESTS.labels(
                method="POST",
                endpoint="/order",
                status="200"
                ).inc()

        return jsonify({"status": "order created"}), 200

    finally:
        INFLIGHT.dec()
        HTTP_LATENCY.labels(endpoint="/order").observe(
                time.time() - start_time
                )

@app.route("/health")
def health():
            APP_HEALTH.set(1)
            HTTP_REQUESTS.labels(
                    method="GET",
                    endpoint="/health",
                    status="200"
                    ).inc()
            return "OK", 200

@app.route("/metrics")
def metrics():
            return generate_latest(), 200, {
                    "Content-Type": "text/plain; version=0.0.4"
                    }

if __name__ == "__main__":
                app.run(host="0.0.0.0", port=8000)
