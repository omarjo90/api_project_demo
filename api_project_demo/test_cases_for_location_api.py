import requests
from urllib.parse import urlencode
import configparser
# Initialize the configparser in order to get credentials from config.ini file
import pytest


config = configparser.ConfigParser()
config.read('./config.ini')

# Global variables
api_key = config['Credentials']['GOOGLE_API_KEY']
place_id = config['Credentials']['PLACE_ID']
place_id2 = config['Credentials']['PLACE_ID2']
rapidapi_key = config['Credentials']['RAPIDAPI_KEY']
base_google_api_url = 'https://maps.googleapis.com/maps/api/'
url = 'https://reqres.in/'


# API Reference: https://developers.google.com/places/web-service/details
# This test verifies name of a place is in the endpoint responce
# using its placeid parameter
def test_google_endpoint_place_details():
    detail_url = 'place/details/json'
    detail_base_endpoint = f'{base_google_api_url}{detail_url}'

    detail_params = {
        'placeid': place_id,
        'fields': 'name,rating,formatted_phone_number',
        'key': api_key
    }

    detail_params_encoded = urlencode(detail_params)

    geocoding_endpoint_url = f'{detail_base_endpoint}?{detail_params_encoded}'
    response = requests.get(geocoding_endpoint_url)

    assert 200 == response.status_code
    assert 'residencial villa bonita'.title() in response.json().get('result').get('name')


# API Reference: https://developers.google.com/maps/documentation/geocoding/overview
# This test verifies that searching address string return valid results
@pytest.mark.parametrize('address', [
    'residencial villa bonita, cartago',
    'UCR, Jardín Botánico Lankester (JBL), Provincia de Cartago, Cartago'
])
def test_google_geocoding_endpoint(address):
    geocoding_url = 'geocode/json'

    #'residencial villa bonita, cartago'
    #UCR, Jardín Botánico Lankester (JBL), Provincia de Cartago, Cartago
    params = {
        'address': address,
        'key': api_key
    }

    url_params = urlencode(params)
    geocoding_endpoint = f'{base_google_api_url}{geocoding_url}?{url_params}'
    response = requests.get(geocoding_endpoint)

    assert response.status_code == 200

    place_id_in_response = response.json().get('results')[0]['place_id']

    if address == 'residencial villa bonita, cartago':
        assert place_id == place_id_in_response
    else:
        assert place_id2 == place_id_in_response


# API Reference: https://developers.google.com/places/web-service/details#PlaceDetailsStatusCodes
# This test verifies the error message returned when API_KEY is wrong
def test_google_error_message_with_incorrect_api_key():
    detail_url = 'place/details/json'
    detail_base_endpoint = f'{base_google_api_url}{detail_url}'

    detail_params = {
        'placeid': place_id,
        'fields': 'name,rating,formatted_phone_number',
        'key': api_key + 'wrong'
    }

    detail_params_encoded = urlencode(detail_params)
    geocoding_endpoint_url = f'{detail_base_endpoint}?{detail_params_encoded}'
    response = requests.get(geocoding_endpoint_url)

    assert 200 == response.status_code
    assert 'The provided API key is invalid.' == response.json()['error_message']
    assert 'REQUEST_DENIED' == response.json().get('status')


# API Reference: https://developers.google.com/maps/documentation/geocoding/overview#StatusCodes
# This test case verifies that entering random string search parameter
# return an error message
def test_google_error_message_with_incorrect_search_address_parameter():
    geocoding_url = 'geocode/json'
    incorrect_address = 'sladlasdlas'

    params = {
        'address': incorrect_address,
        'key': api_key
    }

    url_params = urlencode(params)
    geocoding_endpoint = f'{base_google_api_url}{geocoding_url}?{url_params}'
    response = requests.get(geocoding_endpoint)

    assert response.status_code == 200
    assert 'ZERO_RESULTS' == response.json().get('status')


# API Reference: https://developers.google.com/places/web-service/details#PlaceDetailsStatusCodes
# This test case verifies the error when a required parameter is
# not send in the payload i.e 'placeid'
def test_google_error_message_missing_required_parameter():
    detail_url = 'place/details/json'
    detail_base_endpoint = f'{base_google_api_url}{detail_url}'

    detail_params = {
        'fields': 'name,rating,formatted_phone_number',
        'key': api_key
    }

    detail_params_encoded = urlencode(detail_params)
    geocoding_endpoint_url = f'{detail_base_endpoint}?{detail_params_encoded}'
    response = requests.get(geocoding_endpoint_url)

    assert response.status_code == 200
    assert 'Missing the placeid or reference parameter.' == response.json().get('error_message')
    assert 'INVALID_REQUEST' == response.json().get('status')


# API Reference: https://wirefreethought.github.io/geodb-cities-api-docs/
# This test case verifies 401 status code
# @pytest.mark.skip()
def test_401_unauthorized_error_message():
    incorrect_headers = {
        'Authorization': 'Bearer wrong_bearer_token',
        'x-rapidapi-host': 'wft-geo-db.p.rapidapi.com'
    }
    response = requests.get('https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions?limit=5&offset=0',
                            headers=incorrect_headers)

    assert response.status_code == 401
    assert 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.' in response.json().get('message')


# API Reference: https://wirefreethought.github.io/geodb-cities-api-docs/
# This test case verifies 400 status code
# @pytest.mark.skip()
def test_400_bad_request_error_message():
    headers = {
        'x-rapidapi-key': rapidapi_key,
        'x-rapidapi-host': 'wft-geo-db.p.rapidapi.com'
    }

    url = 'https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions?radius=asas&limit=5&offset=0'

    response = requests.get(url, headers=headers)

    assert response.status_code == 400
    assert 'BAD_REQUEST' in response.json().get('errors')[0].get('code')
    assert 'Failed to convert value of type' in response.json()['errors'][0]['message']


# API Reference: https://gorest.co.in/
# This test case is an example an end to end test for an object
# This object is created, then requested, then updated and finally deleted
# so there are assertions for each scenario
def test_post_get_put_delete_methods_for_object_using_api():
    header = {
        'Authorization': f"Bearer {config['Credentials']['BEARER_TOKEN']}"
    }

    payload = {
        'name': 'QAomar',
        'email': '1omarjo@test.com',
        'status': 'Active',
        'gender': 'Male'
    }

    response = requests.post('https://gorest.co.in/public-api/users', json=payload,
                             headers=header)

    assert response.status_code == 200

    user_id = int(response.json().get('data').get('id'))
    response = requests.get(f'https://gorest.co.in/public-api/users/{user_id}', headers=header)

    assert response.status_code == 200

    update_payload = {
        'name': 'QAomarupdated',
        'email': 'test1@test.com',
        'status': 'Inactive'
    }

    response = requests.put(f'https://gorest.co.in/public-api/users/{user_id}', json=update_payload, headers=header)

    assert response.status_code == 200
    assert 'QAomarupdated' in response.json().get('data').values()

    response = requests.delete(f'https://gorest.co.in/public-api/users/{user_id}', headers=header)

    assert response.status_code == 200


# obtain a user
def test_obtain_user_information():
    response = requests.get(url + 'api/users/2')
    email = response.json().get('data').get('email')
    assert 200 == response.status_code
    assert 'janet.weaver@reqres.in' == email


# create one user
def test_user_creation():
    payload = {
        "name": "qa",
        "job": "automation",
        "skljdjksadhvjklshvfjk": 12313
    }
    response = requests.post(url + 'api/users', json=payload)
    assert 201 == response.status_code
    id_user = response.json().get('id')
    return id_user


# edit one user
def test_edit_one_user():
    payload = {
        "name": "qa updated",
        "job": "updated"
    }
    response = requests.put(url + f'api/users/{test_user_creation()}', json=payload)

    assert response.json().get('job') == payload.get('job')
    assert response.status_code == 200
    assert response.json().get('name') == payload.get('name')


# Delete user
def test_delete_user():
    response = requests.delete(url + f'api/users/{test_user_creation}')
    assert 204 == response.status_code

# #first
# response = requests.get(url+'api/users?page=2')
# print(response.json())
# assert response.status_code == 200
#
# # second
# second_response = requests.get(url + 'api/users/2')
# print(second_response.json())
# assert second_response.status_code == 200
#
# # third
# # Endpoint: /api/users
# # Use this JSON:
# # {
# #     "name": "John",
# #     "job": "Tester"
# # }
#
# payload = {
#     "name": "Omar",
#     "job": "Tester"
# }
#
# third_response = requests.post(url + '/api/users', json=payload)
# print(third_response.json())
# # print(third_response.json().get('id'))
# user_created = third_response.json().get('id')
# assert third_response.status_code == 201
#
# fourth_response = requests.delete(url + f'/api/users/{user_created}')
# print(fourth_response)
# assert fourth_response.status_code == 204
#
# payload = {
#     "job": "Tester"
# }
#
# unsuccessful_response = requests.post(url + '/api/register', json=payload)
# print(unsuccessful_response.json())
# print(unsuccessful_response.status_code)
# assert unsuccessful_response.status_code == 400
