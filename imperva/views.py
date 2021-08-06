from flask import Blueprint, Flask, Response
from flask.views import MethodView
from dotenv import load_dotenv
import os
import json
from pymongo import MongoClient

from .db import DBClient

class CustomersAPI(MethodView, DBClient):
    def __init__(self):
        super().db_client()
        self.db_client = self.db_client().imperva_db

    def get(self, customer_id):
        customers = self.db_client['customers']
        if customer_id is None:
            customer_data = customers.find_one()
            return Response(response=json.dumps(customer_data),
                    status=200,
                    mimetype='application/json')
        else:
            customer_data = customers.find_one({'_id':customer_id})
            if customer_data == None:
                raise Exception('customer with id not found')
                
            return Response(response=json.dumps(customer_data),
                    status=200,
                    mimetype='application/json')

class FilmsAPI(MethodView, DBClient):
    def __init__(self):
        super().db_client()
        self.db_client = db_client().imperva_db

    def get(self, film_id):
        films = self.db_client['films']
        if film_id is None:
            film_data = films.find_one({'_id': film_id})
            return film_data
        else:
            pass
        return "<p>Hello, World!</p>"

