#!/usr/bin/python3
"""
Starts a Flask web application
"""


import os
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """ removes the current SQLAlchemy Session """
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """ displays 9-states.html """
    states = storage.all("State").values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """ displays 9-states.html by id """
    states = storage.all("State")
    state = states.get(id)
    return render_template('9-states.html', state=state)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
