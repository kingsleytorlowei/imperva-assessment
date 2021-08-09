from flask import Blueprint, Flask, Response, request
from flask.views import MethodView
from dotenv import load_dotenv
import os
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

from .db import DBClient
from .utils import create_customer_data, create_film_data
from .exceptions import ImpervaNotFound, ImpervaBadRequest, http_error

class CustomersAPI(MethodView, DBClient):
    def __init__(self):
        self.db_client = self.db_client().imperva_db

    @http_error
    def get(self, customer_id):
        cursor = self.db_client['customers']
        if customer_id is None:
            limit = request.args.get('limit')
            if limit is None or limit == '':
                limit = 10
            offset = request.args.get('offset')
            if offset is None or offset == '':
                offset = 0

            customers_placeholder = []
            all_customers = cursor.find({}).skip(int(offset)).limit(int(limit))
            for customer in all_customers:
                customer_json_data = {}
                customer_json_data['id'] = customer['_id']
                customer_json_data['first_name'] = customer['First Name']
                customer_json_data['last_name'] = customer['Last Name']
                customers_placeholder.append(customer_json_data)
            return Response(response=json.dumps(customers_placeholder),
                    status=200,
                    mimetype='application/json')
        else:
            customer_data = cursor.find_one({'_id':customer_id})
            if customer_data == None:
                raise ImpervaNotFound(f'customer with id: {customer_id} not found')
            cleaned_customer_data = create_customer_data(customer_data)
            return Response(response=json.dumps(cleaned_customer_data),
                    status=200,
                    mimetype='application/json')


class FilmsAPI(MethodView, DBClient):
    def __init__(self):
        self.db_client = self.db_client().imperva_db

    @http_error
    def get(self, film_id):
        film_cursor = self.db_client['films']
        if film_id is None:
            limit = request.args.get('limit')
            if limit is None or limit == '':
                limit = 10
            offset = request.args.get('offset')
            if offset is None or offset == '':
                offset = 0
            films_placeholder = []
            all_films = film_cursor.find({}).skip(int(offset)).limit(int(limit))
            for film in all_films:
                films_json_data = create_film_data(film)
                films_placeholder.append(films_json_data)
            return Response(response=json.dumps(films_placeholder),
                    status=200,
                    mimetype='application/json')
        else:
            customer_cursor = self.db_client['customers']
            film_data = film_cursor.find_one({'_id':film_id})
            if film_data == None:
                raise ImpervaNotFound(f'film with id: {film_id} not found')

            customer_list = []
            all_customers = customer_cursor.find({})
            for customer in all_customers:
                customer_rentals = customer['Rentals']
                for rental in customer_rentals:
                    customer_json_rentals = {}
                    if rental['filmId'] == film_id:
                        customer_json_rentals['id'] = customer['_id']
                        customer_json_rentals['name'] = customer['First Name'].title() + ' ' + customer['Last Name'].title()
                        customer_list.append(customer_json_rentals)

            film_response_data = create_film_data(film_data)
            film_response_data['film_length'] = film_data['Length']
            film_response_data['replacement_cost'] = film_data['Replacement Cost']
            film_response_data['special_features'] = film_data['Special Features']
            film_response_data['customers'] = customer_list

            return Response(response=json.dumps(film_response_data),
                    status=200,
                    mimetype='application/json')
