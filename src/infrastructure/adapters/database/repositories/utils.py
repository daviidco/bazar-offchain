from datetime import datetime

import requests


def get_role_user(access_token):
    pass


def default_prefix_cloud():
    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))


def get_user_names(jwt, uuid_user) -> tuple:
    first_name = 'undefined'
    last_name = 'undefined'
    url = f"https://meerkat-auth.herokuapp.com/api/v1/user/person/uuid/{uuid_user}"
    headers = {
        'accept': '*/*',
        'Authorization': f'{jwt}'
    }

    response_auth = requests.request("GET", url, headers=headers)
    data_response = response_auth.json()['data']
    if data_response is not None:
        first_name = data_response['firstName']
        last_name = data_response['lastName']
    return first_name, last_name
