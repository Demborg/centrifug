from queue import Queue
from typing import Sequence

from flask import Flask, Response, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

listeners = [] # type: Sequence[Queue]

descriptions = {
    "01.mp4" : {
        "title": "Genuary 01 - Perfect loop",
        "medium": "Blender",
        "text": ""
    },
    "02.mp4" : {
        "title": "Genuary 02 - 10 minutes",
        "medium": "Blender",
        "text": ""
    },
    "03.mp4" : {
        "title": "Genuary 03 - Glitch",
        "medium": "Audacity, Spreadsheets",
        "text": "A circular path in the frequency/Q-space of a notch filter applied to a self portrait."
    },
    "04.mp4" : {
        "title": "Genuary 04 - Intersections",
        "medium": "Blender",
        "text": ""
    },
    "05.mp4" : {
        "title": "Genuary 05 - Debug UI",
        "medium": "Blender",
        "text": ""
    },
    "06.mp4" : {
        "title": "Genuary 06 - Steal like an artis",
        "medium": "Blender",
        "text": ""
    },
    "07.mp4" : {
        "title": "Genuary 07 - Däggdjur",
        "medium": "Python",
        "text": ""
    }
}

@app.route("/broadcast/<value>")
def broadcast(value: str):
    for l in listeners:
        l.put_nowait(value)
    return render_template("page.html", video=value, info=descriptions[value])

@app.route("/listen")
def listen():
    def stream():
        message_queue = Queue()
        listeners.append(message_queue)
        while True:
            msg =  message_queue.get()
            yield f"data: {msg}\n\n"
    return Response(stream(), mimetype="text/event-stream")