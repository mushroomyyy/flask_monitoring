import time
import redis
from flask import Flask
import os
from prometheus_flask_exporter import PrometheusMetrics
# Explicitly import Gauge from the underlying client library
from prometheus_client import Gauge

app = Flask(__name__)
metrics = PrometheusMetrics(app) # Initialize exporter

# Static information as metric
metrics.info('app_info', 'Application info', version='1.0.1') # Incremented version for clarity

# --- MODIFICATION START ---
# Define the gauge using the core prometheus_client library first
# We register with the exporter's registry to ensure it's exposed
redis_conn_gauge = Gauge(
    'redis_connection_status', # Slightly different name just in case
    'Indicates if Redis connection is healthy (1=yes, 0=no)',
    registry=metrics.registry # Use the exporter's registry
)
# --- MODIFICATION END ---

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
cache = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            # Check connection and set gauge using the new variable name
            cache.ping()
            redis_conn_gauge.set(1) # <-- Use new variable name
            # Increment the counter
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            redis_conn_gauge.set(0) # <-- Use new variable name
            if retries == 0:
                app.logger.error(f"Could not connect to Redis at {redis_host}:{redis_port} after multiple retries.")
                raise exc
            retries -= 1
            app.logger.warning(f"Redis connection error, retrying in 0.5s... ({retries} retries left)")
            time.sleep(0.5)
        except Exception as e:
            redis_conn_gauge.set(0) # <-- Use new variable name
            app.logger.error(f"An error occurred with Redis: {e}")
            return "Error interacting with cache"

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\n'

# The metrics endpoint is automatically added at /metrics by the exporter

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)