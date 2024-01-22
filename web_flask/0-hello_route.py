#!/usr/bin/python3
"""
Starting a flask web app in localhost
"""


from flask import Flask
app = Flask(__name__)


@app.route('/airbnb-onepage/', strict_slashes=False)
def index():
    """
    Display hello HBNB
    """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(port=5000)
