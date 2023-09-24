#!/usr/bin/python3
"""Define a route that displays "Hello HBNB!" when you access the root URL ("/")
"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb_route():
    return "Hello HBNB!"

# Start the Flask web application, listening on 0.0.0.0 and port 5000
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
