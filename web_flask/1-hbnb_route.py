#!/usr/bin/python3
"""script that starts a Flask web application
"""
from flask import Flask
app = Flask(__name__)

# route that displays "Hello HBNB!" when you access the root ('/')
@app.route("/", strict_slashes=False)
def hello_hbnb_route():
    return "Hello HBNB!"

# Define a route that displays "HBNB" when you access the "/hbnb" URL
@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    return "HBNB"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
