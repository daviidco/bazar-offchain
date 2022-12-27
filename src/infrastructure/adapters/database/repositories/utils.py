import json
from datetime import datetime

import requests
from flask import current_app
from flask_restx import abort
from sqlalchemy.orm import Session

from src.infrastructure.adapters.database.models import User, Company, Product
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.config.config_parameters import get_parameter_value

URL_MS_BAZAR_AUTH = get_parameter_value('URL_MS_BAZAR_AUTH')
URL_EMAIL_LAMBDA = get_parameter_value('URL_EMAIL_LAMBDA')
AWS_BUCKET_NAME = get_parameter_value('AWS_BUCKET_NAME')
AWS_REGION = current_app.config['AWS_REGION']


def default_prefix_cloud():
    path_datetime = str(datetime.today().strftime('%Y/month-%m/day-%d/%I-%M-%S'))


def build_urls_from_profile_image(profile_image):
    # Urls profile images
    profile_images = []
    if profile_image is not None:
        if profile_image.image_url is not None:
            idx_last_dot = profile_image.image_url.rindex('.')
            format_file = profile_image.image_url[idx_last_dot:]
            url_base = profile_image.image_url[:idx_last_dot - 2]
            profile_images.append(f"{url_base}-s{format_file}")
            profile_images.append(f"{url_base}-m{format_file}")
            profile_images.append(f"{url_base}-b{format_file}")
    return profile_images


def build_urls_from_url_image(url_image):
    profile_images = []
    if url_image is None:
        return []
    idx_last_dot = url_image.rindex('.')
    format_file = url_image[idx_last_dot:]
    url_base = url_image[:idx_last_dot - 2]
    profile_images.append(f"{url_base}-s{format_file}")
    profile_images.append(f"{url_base}-m{format_file}")
    profile_images.append(f"{url_base}-b{format_file}")
    return profile_images


def build_url_bd(prefix, name):
    file_name = name.replace('+', '%2B').replace(' ', '+')
    key_bd = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{prefix}/{file_name}"
    return key_bd


def build_url_storage(prefix, name):
    key_storage = f"{prefix}/{name}"
    return key_storage


def request_to_ms_auth(jwt, uuid_user, get_person=False):
    base_url = URL_MS_BAZAR_AUTH
    headers = {
        'accept': '*/*',
        'Authorization': f'{jwt}'
    }
    url = f"{base_url}/person/uuid/{uuid_user}"

    response_auth = requests.request("GET", url, headers=headers)
    if 200 < response_auth.status_code < 300 and get_person:
        uuid_person = response_auth.json()['data']['uuid']
        url = f"{base_url}/email/uuidperson/{uuid_person}"
        response_auth = requests.request("GET", url, headers=headers)

    if 200 < response_auth.status_code < 300:
        data_response = response_auth.json()['data']
        return data_response
    else:
        current_app.logger.critical(f"Error getting info ms-auth - code response: {response_auth.status_code}")
        return None


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
        url = URL_EMAIL_LAMBDA

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


def get_total_pages(total_elements: int, limit: int):
    if total_elements == limit:
        return 1
    elif total_elements == 0:
        return 0
    return (total_elements // limit) + 1


def validate_num_certifications_vs_num_files(num_certs: int, num_files: int):
    if num_certs != num_files:
        e = api_error('NumCertificationsVSNumFilesError')
        description = e.error.get('description', 'Not description')
        current_app.logger.error(f"{description}")
        abort(code=e.status_code, message=e.message, error=e.error)


class UtilsDatabase:
    def __init__(self, adapter_db):
        self.engine = adapter_db.engine
        self.session = Session(adapter_db.engine)

    def get_user_by_uuid_user(self, uuid_user):
        user = self.session.query(User).filter_by(uuid=uuid_user).first()
        if user is None:
            e = api_error('ObjectNotFound')
            e.error['description'] = e.error['description'] + f' <user uuid_user: {uuid_user}>'
            current_app.logger.error(e.error['description'])
            abort(code=e.status_code, message=e.message, error=e.error)
        return user

    def get_company_by_uuid_user(self, uuid_user):
        user = self.get_user_by_uuid_user(uuid_user)
        company = self.session.query(Company).filter_by(user_id=user.id).first()
        if company is None:
            e = api_error('ObjectNotFound')
            e.error['description'] = e.error['description'] + f' <company uuid_user: {uuid_user}>'
            current_app.logger.error(e.error['description'])
            abort(code=e.status_code, message=e.message, error=e.error)
        return company

    def get_product_by_uuid_product(self, uuid_product):
        product = self.session.query(Product).filter_by(uuid=uuid_product).first()
        if product is None:
            e = api_error('ObjectNotFound')
            e.error['description'] = e.error['description'] + f' <product uuid_product: {uuid_product}>'
            current_app.logger.error(e.error['description'])
            abort(code=e.status_code, message=e.message, error=e.error)
        return product


