from flask import Blueprint, Flask, Response, request
from flask.views import MethodView
from dotenv import load_dotenv
import os
import json
from pymongo import MongoClient

from .db import DBClient
from .utils import create_customer_data, create_film_data

class CustomersAPI(MethodView, DBClient):
    def __init__(self):
        self.db_client = self.db_client().imperva_db

    def get(self, customer_id):
        cursor = self.db_client['customers']
        if customer_id is None:
            limit = int(request.args.get('limit'))
            if limit is None or limit == '':
                limit = 0
            offset = int(request.args.get('offset'))
            if offset is None or offset == '':
                offset = 0
            customers_placeholder = []
            all_customers = cursor.find({}).skip(offset).limit(limit)
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
                raise Exception('customer with id not found')
            cleaned_customer_data = create_customer_data(customer_data)
            return Response(response=json.dumps(cleaned_customer_data),
                    status=200,
                    mimetype='application/json')


class FilmsAPI(MethodView, DBClient):
    def __init__(self):
        self.db_client = self.db_client().imperva_db

    def get(self, film_id):
        cursor = self.db_client['films']
        if film_id is None:
            film_data = cursor.find_one({'_id': film_id})
            return film_data
        else:
            film_data = cursor.find_one({'_id':film_id})
            if film_data == None:
                raise Exception('film with id not found')
            cleaned_rental_data = create_film_data(film_data)
            return Response(response=json.dumps(cleaned_rental_data),
                    status=200,
                    mimetype='application/json')
