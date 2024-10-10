"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
# from http import HTTPStatus

from flask import Flask, request  # , request
from flask_restx import Resource, Api, fields  # Namespace , fields
from flask_cors import CORS

import data.people as ppl
from data.people import people_dict

# import werkzeug.exceptions as wz

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
TITLE_EP = '/title'
TITLE_RESP = 'Title'
TITLE = 'Journal About Ocean'
PEOPLE_EP = '/people'

person_model = api.model('Person', {
    'name': fields.String(required=True, description='The person\'s name'),
    'affiliation': fields.String(required=True, description='The person\'s affiliation'),
    'email': fields.String(required=True, description='The person\'s email')
})


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(TITLE_EP)
class JournalTitle(Resource):
    """
    This class handles creating, reading,
     updating, and deleting the journal title.
    """
    def get(self):
        """
        Retrieve the journal title
        """
        return {TITLE_RESP: TITLE}


@api.route(f'{PEOPLE_EP}/<path:email>')
# @api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, reading, updating
    and deleting journal people.
    """
    def get(self):
        """
        Retrieve the journal people.
        """
        return ppl.get_people()

    @api.expect(person_model)
    def put(self):
        """
        Update an existing person.
        """
        data = api.payload
        try:
            updated_person = ppl.update_person(
                data['name'],
                data['affiliation'],
                data['email'])
            return {'message': 'Person updated successfully',
                    'person': updated_person}, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.expect(person_model)
    def post(self):
        """
        Create a new person.
        """
        data = request.json
        try:
            new_person = ppl.create_person(
                data['name'],
                data['affiliation'],
                data['email'])  #
            return {'message': 'Person created successfully',
                    'person': new_person,
                    }, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    def get(self, email=None):
        '''
        read an existing person
        '''
        try:
            person = ppl.read_person(email)
            return person, 200
        except ValueError as e:
            return {'message': str(e)}, 404
