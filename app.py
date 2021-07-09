from flask import Flask, send_file, request, Response
from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest, start_http_server

import logging
import prometheus_apsystem

logger = logging.getLogger(__name__)

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

@app.route('/metrics', methods=['GET'])
def get_data():
    """Returns all data as plaintext."""
    registry = CollectorRegistry()
    # multiprocess.MultiProcessCollector(registry)
    data = generate_latest(prometheus_apsystem.stronaglowna(registry))
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')