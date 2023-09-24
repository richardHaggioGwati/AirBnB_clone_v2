#!/usr/bin/python3
"""# Define a route that takes a dynamic parameter 'text' 
(with a default value of "is cool") and displays "Python" 
followed by the value of 'text' (replace underscore _ symbols with a space)
"""
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb_route():
    return "Hello HBNB!"

@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    return "HBNB"

@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    return "C {}".format(text.replace('_', ' '))

@app.route("/python/", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text='is cool'):
    return "Python {}".format(text.replace('_', ' '))

@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    return "{} is a number".format(n)

# Render template
@app.route("/number_template/<int:n>", strict_slashes=False)
def int_template(n):
    return render_template('5-number.html', number=n)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
