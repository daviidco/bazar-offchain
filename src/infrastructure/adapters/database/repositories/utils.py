from datetime import datetime

import requests
from flask_restx import abort
from sqlalchemy.orm import Session

from src.infrastructure.adapters.database.models import User, Company
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


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
