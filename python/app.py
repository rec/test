from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/one/<two>")
def one(two):
    return f"<pre>{two}</pre>"
