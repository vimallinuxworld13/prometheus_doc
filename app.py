#pip3 install flask
#   7  yum install python3-pip
#   8  pip3 install flask
#   9  pip3 install prometheus-client
from flask import Flask

from prometheus_client import Counter, Gauge, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter(
                    "lw_total_request",
                    "Total App request till date desc..",
                    ['method', 'endpoint']
                    )

APP_STATUS = Gauge("lw_app_status", "Application status up - 1 or down - 0")


@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    APP_STATUS.set(1)
    print(REQUEST_COUNT)
    return "welcome to LW.."

@app.route("/metrics")
def metrics():
    return generate_latest(), 200 , {
                "Content-type": "text/plain"
            }




app.run(host="0.0.0.0", port=8000)
