#!/usr/bin/env python3
import json
import logging
import argparse

from flask import Flask, session, redirect, url_for, escape, request, jsonify

from apispec import APISpec
from apispec.utils import validate_swagger
from marshmallow import Schema, fields

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Create an APISpec
spec = APISpec(
    title='opeb-submission-api',
    version='0.0.1',
    openapi_version='3.0.0',
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
    # app.run()

    parser = argparse.ArgumentParser(description='opeb-submission-api')
    parser.add_argument(
        "mode", choices=['spec', 'api'], help="Generate OpenAPIv3 spec | Launch the opeb-submission-api", type=str)
    args = parser.parse_args()
    if args.mode == 'spec':
        spec_filename = 'opeb-submission-api.json'
        try:
            validate_swagger(spec)
            with open(f'public/spec/{spec_filename}', 'w') as api_file:
                json.dump(spec.to_dict(), api_file, indent=2, sort_keys=True)
            print(
                f'\033[32m{spec_filename} spec generated and validated against OpenAPIv3 succesfully!\033[0m')
        except:
            print(
                f"\033[31mError: {spec_filename} couldn't be validated against OpenAPIv3!\033[0m", file=sys.stderr)
    elif args.mode == 'api':
        print('API')
