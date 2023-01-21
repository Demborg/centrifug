from flask import Flask

app = Flask(__name__)

cache = {"value": "hej"}

@app.route("/set/<value>")
def set(value: str):
    cache["value"] = value
    return f"set value {value}"

@app.route("/")
def hello_world():
    return cache["value"]