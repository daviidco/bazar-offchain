from datetime import datetime

import requests
from flask_restx import abort
from sqlalchemy.orm import Session

from src.infrastructure.adapters.database.models import User, Company
from flask import current_app
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error

import json

def default_prefix_cloud():
    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))


def request_to_ms_auth(jwt, uuid_user, get_person=False):
    base_url = "https://meerkat-auth.herokuapp.com/api/v1/user"
    headers = {
        'accept': '*/*',
        'Authorization': f'{jwt}'
    }
    url = f"{base_url}/person/uuid/{uuid_user}"

    response_auth = requests.request("GET", url, headers=headers)
    if get_person:
        uuid_person = response_auth.json()['data']['uuid']
        url = f"{base_url}/email/uuidperson/{uuid_person}"
        response_auth = requests.request("GET", url, headers=headers)
        data_response = response_auth.json()['data']
        return data_response

    data_response = response_auth.json()['data']
    return data_response


def get_user_names(jwt, uuid_user) -> tuple:
    first_name = 'undefined'
    last_name = 'undefined'
    data_response = request_to_ms_auth(jwt, uuid_user)
    if data_response is not None:
        first_name = data_response['firstName']
        last_name = data_response['lastName']
    return first_name, last_name


def get_email(jwt, uuid_user) -> str:
    email = 'undefined'
    data_response = request_to_ms_auth(jwt, uuid_user, True)
    if data_response is not None:
        email = data_response['email']
    return email


def send_email(subject: str, data: str, destination: list, is_html: bool = False) -> bool:
    try:
        type_content = "Html" if is_html else "Text"
        url = "https://30mtgv2761.execute-api.us-east-2.amazonaws.com/dev/create"

        payload = json.dumps({
            "user_id": "123456",
            "noti_data": {
                "email": "systems@bazar.network",
                "source": "systems@bazar.network",
                "destination": destination,
                "subject": {
                    "Data": subject,
                    "Charset": "UTF-8"
                },
                "message": {
                    type_content: {
                        "Data": data,
                        "Charset": "UTF-8"
                    }
                },
                "status": "awaiting"
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        result = True if response.status_code == 200 else False
        if not result:
            raise Exception('Not implemented method')
        current_app.logger.info(f"OK - Email sent to {destination}")
        return result

    except Exception as e:
        current_app.logger.error(f"Error Sending email to {destination} - {str(e)}")
        e = api_error('EmailError')
        abort(code=e.status_code, message=e.message, error=e.error)


class UtilsDatabase:
    def __init__(self, logger, adapter_db):
        self.logger = logger
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)

    def get_company_by_uuid_user(self, uuid_user):
        user = self.session.query(User).filter_by(uuid=uuid_user).first()
        if user is None:
            e = api_error('ObjectNotFound')
            e.error['description'] = e.error['description'] + ' <user>'
            abort(code=e.status_code, message=e.message, error=e.error)

        company = self.session.query(Company).filter_by(user_id=user.id).first()
        if company is None:
            e = api_error('ObjectNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)
        return company
