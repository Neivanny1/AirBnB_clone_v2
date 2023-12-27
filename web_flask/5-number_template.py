#!/usr/bin/python3
"""
Starts a Flask web application
"""


from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    Displays Hello HBNB!
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Displays HBNB!
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def show_c(text):
    """
    Show c
    """
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def show_python(text='is cool'):
    """
    Show python
    """
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def is_integer(n):
    """
    Show is integer
    """
    return "{} is a number".format(n)


@app.route('/number_templates/<int:n>', strict_slashes=False)
def number_templates(n):
    """
    Rendering html templates
    """
    num = {'n': n}
    return render_template('5-number.html', **num)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
