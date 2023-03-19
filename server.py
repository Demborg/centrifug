from queue import Queue
from typing import Sequence
from datetime import datetime
from pathlib import Path

from flask import Flask, Response, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

database = Path("database.csv")

listeners = [] # type: Sequence[Queue]

descriptions = {
    "01.mp4" : {
        "title": "Genuary 01 - Cold welding",
        "medium": "Blender",
        "text": "Exploring scale ambiguity with an endlessly looping zoom."
    },
    "01-1.mp4" : {
        "title": "Scanning",
        "medium": "Blender",
        "text": "Earlier experiments with endlessly looping cubes."
    },
    "02.mp4" : {
        "title": "Genuary 02 - 10 minutes",
        "medium": "Blender",
        "text": "Hours spent trying to polish a piece that was meant to be done in 10 minutes."
    },
    "03.mp4" : {
        "title": "Genuary 03 - Glitch",
        "medium": "Audacity, Spreadsheets",
        "text": "A circular path in the frequency/Q-space of a notch filter applied to a self portrait."
    },
    "03-1.mp4" : {
        "title": "Dithering",
        "medium": "Blender",
        "text": "Dithering by casting shadows from moving balls."
    },
    "03-2.mp4" : {
        "title": "En krokus, flera kroki",
        "medium": "Blender, Photography",
        "text": "A bad pun begging to become art through nudity."
    },
    "04.mp4" : {
        "title": "Genuary 04 - Intersections",
        "medium": "Blender",
        "text": "Briliant intersections of soap bubbles."
    },
    "05.mp4" : {
        "title": "Genuary 05 - Debug UI",
        "medium": "Blender",
        "text": "Visualizing the indices and offset fields driving the bubbles from 04."
    },
    "06.mp4" : {
        "title": "Genuary 06 - Steal like an artis",
        "medium": "Blender",
        "text": "Stealing and animating the beutifull irises by Ulla Wiggen."
    },
    "06-1.mp4" : {
        "title": "Cheap copies 01 - Sliding Zeus XL",
        "medium": "Blender",
        "text": "Trying to recreate Sliding Zeus XL by Andreas Wannerstedt in my favourite software."
    },
    "06-2.mp4" : {
        "title": "Cheap copies 02 - Chromie Squiggle",
        "medium": "Blender",
        "text": "Trying to recreate the Chromeie Squiggles by Archipelago in my favourite software."
    },
    "06-3.mp4" : {
        "title": "Cheap copies 03 - The red spot",
        "medium": "Blender",
        "text": "Trying to recreate The Red Spot by Six N. Five in my favourite software."
    },
    "07.mp4" : {
        "title": "Genuary 07 - Däggdjur",
        "medium": "Python",
        "text": "Sampling a bit more than the palette from \"Däggdjur\", maybe the greatest album of all time."
    }
}

@app.route("/broadcast/<value>")
def broadcast(value: str):
    for l in listeners:
        l.put_nowait(value)

    with database.open("a") as file:
        file.write(f"{datetime.now()},{value}\n")
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

@app.route("/stats")
def stats():
    return database.read_text() if database.is_file() else ""
