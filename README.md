# Imperva-Assessment

# How to Run 

Start by opening root directory.

## Create Virtual Enviroment
```
python3 -m venv env
```

## Activate Virtual Enviroment
```
source env/bin/activate
```

## Install dependencies
```
pip install -r requirements.txt
```

## Run code
```
flask run
```
## Documentation
```
Documentation can be found in the doc/ directory of the root directory. Import to postman, create a new postman enviroment and make the base_url enviroment variable: `http://127.0.0.1:5000/api`
```
## Considerations and Limitations 
 * Make sure you create virtual enviroment before running application. 
 * A good understanding of flask is required to know how the application works. 
 * Multiple configurations need to be created to support a testing framework for the application.
 * A mechanism to create and test database's also needed to test the application and persist test data between test as the endpoints grow.