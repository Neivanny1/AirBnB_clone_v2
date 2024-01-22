#!/usr/bin/python3
"""
Starts a Flask web application
"""
import os
from flask import Flask, render_template
from markupsafe import Markup
from models import storage
from models.amenity import Amenity
from models.state import State
from models.place import Place

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Displays a list of states
    """
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda state: state.name)

    return render_template('7-states_list.html', states=states_sorted)


@app.teardown_appcontext
def flask_teardown(exc):
    '''The Flask app/request context end event listener.'''
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page with States"""
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states')
@app.route('/states/<id>')
def states(id=None):
    """
    The states page
    """
    states = None
    state = None
    all_states = list(storage.all(State).values())
    case = 404
    if id is not None:
        res = list(filter(lambda x: x.id == id, all_states))
        if len(res) > 0:
            state = res[0]
            state.cities.sort(key=lambda x: x.name)
            case = 2
    else:
        states = all_states
        for state in states:
            state.cities.sort(key=lambda x: x.name)
        states.sort(key=lambda x: x.name)
        case = 1
    ctxt = {
        'states': states,
        'state': state,
        'case': case
    }
    return render_template('9-states.html', **ctxt)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    The hbnb_filters page
    """
    all_states = list(storage.all(State).values())
    amenities = list(storage.all(Amenity).values())
    all_states.sort(key=lambda x: x.name)
    amenities.sort(key=lambda x: x.name)
    for state in all_states:
        state.cities.sort(key=lambda x: x.name)
    ctxt = {
        'states': all_states,
        'amenities': amenities
    }
    return render_template('10-hbnb_filters.html', **ctxt)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

