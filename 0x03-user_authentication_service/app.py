#!/usr/bin/env python3
"""Web server Flask set up."""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """Returns a message for index route '/'.

    response - message: Bienvenue"""
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
