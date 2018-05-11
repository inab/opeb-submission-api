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
    return 'Index'


@app.route('/submissions')
def submissions():
    """Submissions endpoint.
    ---
    get:
        description: Submissions endpoint description
        responses:
            200:
                description: It returns the submissions associated to the participants identified by the login credentials (the same credential could manage more than one participant), as a JSON array of URIs in the form /submission/{benchmarking event id}/{participant id}/status.


    """
    return 'TODO: submissions'


with app.test_request_context():
    spec.add_path(view=index)
    spec.add_path(view=submissions)

if __name__ == '__main__':

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
        app.run()
