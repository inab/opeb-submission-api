#!/usr/bin/env python3
import json
import logging

from flask import Flask, session, redirect, url_for, escape, request, jsonify

from apispec import APISpec
from marshmallow import Schema, fields

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Create an APISpec
spec = APISpec(
    title='opeb-submission-api',
    version='0.0.1',
    plugins=[
        'apispec.ext.flask',
        'apispec.ext.marshmallow',
    ],
)


@app.route('/')
def index():
    """Index endpoint.
    ---
    get:
        description: Index endpoint description
        responses:
            200:
                description: returned index string
                type: string

    """
    if 'username' in session:
        return 'index<br><br>Logged in as %s' % escape(session['username'])
    return 'index<br><br>You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
      <form method="post">
          <p><input type=text name=username>
          <p><input type=submit value=Login>
      </form>
  '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

with app.test_request_context():
    spec.add_path(view=index)

if __name__ == '__main__':
    print(spec.to_dict())
    app.run()
