import os

from flask import Flask, Response
from dotenv import dotenv_values
from .views import CustomersAPI, FilmsAPI


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    config = dotenv_values(".env")
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config.update(config)

    def register_api(view, endpoint, url, pk='id', pk_type='int'):
        view_func = view.as_view(endpoint)
        app.add_url_rule(url, defaults={pk: None},view_func=view_func, methods=['GET'])
        app.add_url_rule(f'{url}<{pk_type}:{pk}>/', view_func=view_func, methods=['GET'])
  
    register_api(CustomersAPI, 'customer_api', '/customers/', pk='customer_id')
    register_api(FilmsAPI, 'film_api', '/films/', pk='film_id')
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def base():
        return Response(response=json.dumps({"Status": "UP"}),
                    status=200,
                    mimetype='application/json')

    return app

