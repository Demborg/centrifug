from queue import Queue
from typing import Sequence

from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

listeners = [] # type: Sequence[Queue]

@app.route("/broadcast/<value>")
def broadcast(value: str):
    for l in listeners:
        l.put_nowait(value)
    return f"broadcasting value {value}"

@app.route("/listen")
def listen():
    def stream():
        message_queue = Queue()
        listeners.append(message_queue)
        while True:
            msg =  message_queue.get()
            yield f"data: {msg}\n\n"
    return Response(stream(), mimetype="text/event-stream")