#!/usr/bin/python3
"""
Module for simple Flask web application
"""
from flask import Flask, render_template
from markupsafe import Markup

from models import storage
from models.amenity import Amenity
from models.place import Place
from models.state import State


app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    The hbnb home page
    """
    all_states = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    places = list(storage.all(Place).values())
    all_states.sort(key=lambda x: x.name)
    amenities.sort(key=lambda x: x.name)
    places.sort(key=lambda x: x.name)
    for state in all_states:
        state.cities.sort(key=lambda x: x.name)
    for place in places:
        place.description = Markup(place.description)
    ctxt = {
        'states': all_states,
        'amenities': amenities,
        'places': places
    }
    return render_template('100-hbnb.html', **ctxt)


@app.teardown_appcontext
def flask_teardown(exc):
    """
    The Flask app/request context end event listener
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
