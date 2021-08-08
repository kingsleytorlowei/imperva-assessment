from datetime import datetime

def calculate_rental_duration(rental_date, return_date):
    rental_date_object = datetime.strptime(rental_date, '%Y-%m-%d %H:%M:%S.0')
    return_date_object = datetime.strptime(return_date, '%Y-%m-%d %H:%M:%S.0')
    rental_duration = return_date_object - rental_date_object
    rental_duration_days = rental_duration.days
    return str(rental_duration_days) + ' days'

def calculate_rental_cost(rental_payments):
    payment_amount = 0
    for payment in rental_payments:
        payment_amount += payment['Amount']
    return round(payment_amount, 2)

def clean_rental_information(rentals):
    rentals_list = []
    for rental in rentals:
        rental_info = {}
        rental_info['film_title'] = rental['Film Title'].lower()
        rental_info['rental_duration'] = calculate_rental_duration(rental['Rental Date'], rental['Return Date'])
        rental_info['rental_cost'] = calculate_rental_cost(rental['Payments'])
        rentals_list.append(rental_info)
    return rentals_list



def create_customer_data(customer_json_data):
    customer_json = {}
    customer_json['address'] = customer_json_data['Address'].lower()
    customer_json['city'] = customer_json_data['City'].lower()
    customer_json['country'] = customer_json_data['Country'].lower()
    customer_json['first_name'] = customer_json_data['First Name'].title()
    customer_json['last_name'] = customer_json_data['Last Name'].title()
    customer_json['rentals'] = clean_rental_information(customer_json_data['Rentals'])
    return customer_json


def create_film_data(film_data):
    cleaned_film_data = {}
    cleaned_film_data['id'] = film_data['_id']
    cleaned_film_data['title'] = film_data['Title'].lower()
    cleaned_film_data['category'] = film_data['Title'].lower()
    cleaned_film_data['description'] = film_data['Description'].lower()
    cleaned_film_data['rating'] = film_data['Rating'].lower()
    cleaned_film_data['rental_duration'] = film_data['Rental Duration'].lower()
    return cleaned_film_data