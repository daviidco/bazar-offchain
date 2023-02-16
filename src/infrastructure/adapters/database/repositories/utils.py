# -*- coding: utf-8 -*-
#
# This source code is the confidential, proprietary information of
# Bazar Network S.A.S., you may not disclose such Information,
# and may only use it in accordance with the terms of the license
# agreement you entered into with Bazar Network S.A.S.
#
# 2022: Bazar Network S.A.S.
# All Rights Reserved.
#

import json

import requests
from flask import current_app, render_template
from flask_restx import abort
from flask_restx.reqparse import request
from sqlalchemy.orm import sessionmaker

from src.domain.entities.product_entity import ProductEntity
from src.infrastructure.adapters.database.models import User, Company, Product
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.config.config_parameters import get_parameter_value
from src.infrastructure.config.default import URL_EMAIL_LAMBDA, URL_MS_BAZAR_AUTH, AWS_REGION, LINK_BAZAR, ORIGIN_EMAIL
from src.infrastructure.templates_email import TemplateAdminProduct

#
# This file contains utils functions to be used to global level
# @author David Córdoba
#

AWS_BUCKET_NAME = get_parameter_value('AWS_BUCKET_NAME')


def admin_emails():
    admins_email = current_app.config['EMAIL_BAZAR_ADMIN'].split(';')
    return admins_email


def truncate_name(name: str, max_len: int = 20) -> str:
    """
    Function to truncate long names with extension.
    When is a name file to concatenate as URL is advisable a max_len of 16 characters
    :param max_len: len max of result
    :param name: origin name
    :return: new name truncated
    """
    list_name = name.split('.')
    list_name[0] = list_name[0][:max_len]
    result_name = '.'.join(list_name)
    return result_name


def build_urls_from_profile_image(profile_image):
    """
    Build urls to profile images
    :param profile_image: profile image
    :return: list of urls profile images
    """
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
    """
    Build urls from one url image
    :param url_image: url image
    :return: list of urls profile images
    """
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
    """
    Function return complete url where will be saved the objet
    :param prefix: prefix url
    :param name: name object
    :return: url to bd
    """
    file_name = name.replace('+', '%2B').replace(' ', '+')
    key_bd = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{prefix}/{file_name}"
    return key_bd


def build_url_storage(prefix, name):
    """
    Function return partial url where will be saved the object
    :param prefix: prefix url
    :param name: name object
    :return: key storage
    """
    key_storage = f"{prefix}/{name}"
    return key_storage


def request_to_ms_auth(uuid_user, get_person=False):
    """
    Function that do request to bazar-auth
    :param jwt: json web token to get username of bazar-auth
    :param uuid_user: uuid user to get username of bazar-auth
    :param get_person: boolean flag determines call endpoint user o endpoint person
    :return: response data from bazar-auth
    """
    jwt = dict(request.headers).get('Authorization', None)
    base_url = URL_MS_BAZAR_AUTH
    headers = {
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


def get_user_names(uuid_user) -> tuple:
    """
    Function to get email from bazar-auth
    :param uuid_user: uuid user to get username of bazar-auth
    :return: firstname and lastname like tuple
    """
    first_name = 'undefined'
    last_name = 'undefined'
    data_response = request_to_ms_auth(uuid_user)
    if data_response is not None:
        first_name = data_response['firstName']
        last_name = data_response['lastName']
    return first_name, last_name


def get_email(uuid_user) -> str:
    """
    Function to get email from bazar-auth
    :param uuid_user: uuid user to get username of bazar-auth
    :return: email in format str
    """
    email = 'undefined'
    data_response = request_to_ms_auth(uuid_user, True)
    if data_response is not None:
        email = data_response['email']
    return email


def get_whatsapp_phone(uuid_user) -> tuple:
    """
    Function to get whatsapp phone from bazar-auth. Bazar-auth check phone number was checked as whatsapp phone
    :param uuid_user: uuid user to get username of bazar-auth
    :return: whatsapp phone
    """
    data_response = request_to_ms_auth(uuid_user)
    if data_response is not None:
        if data_response['user']['active']:
            whatsapp_phone = data_response['phoneNumber']
            return whatsapp_phone


def send_email(subject: str, data: str, destination: list, is_html: bool = False) -> bool:
    """
    Generic function to send email
    :param subject: subject of email
    :param data: data of email
    :param destination: list of recipients
    :param is_html: boolean flag to determinate type of content email
    :return: boolean True if email sending was successful else False
    """
    try:
        type_content = "Html" if is_html else "Text"
        url = URL_EMAIL_LAMBDA

        payload = json.dumps({
            "user_id": "123456",
            "noti_data": {
                "email": ORIGIN_EMAIL,
                "source": ORIGIN_EMAIL,
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
    """
    Function to get total number pages of endpoints with pagination
    :param total_elements: total elements from query
    :param limit: limit elements specified by client
    :return: total number pages
    """
    if total_elements == limit:
        return 1
    elif total_elements == 0:
        return 0
    return (total_elements // limit) + 1


def validate_num_certifications_vs_num_files(num_certs: int, num_files: int):
    """
    Function to validate tha the number certifications checked is equal to number files will be uploaded
    :param num_certs: number certifications
    :param num_files: number files to upload to storage
    :return: abort application if they are not equals
    """
    current_app.logger.info(f"Checking num certifications vs num files uploaded ")
    if num_certs != num_files:
        e = api_error('NumCertificationsVSNumFilesError')
        description = e.error.get('description', 'Not description')
        current_app.logger.error(f"{description}")
        abort(code=e.status_code, message=e.message, error=e.error)


def send_email_to_admin(uuid_user, product, prefix_files):
    """
    Function to send email to admin like notification when a product was registered with certifications
    :param uuid_user: uuid user to get username of bazar-auth
    :param product: product with information to email body
    :param prefix_files: path in storage
    """
    # Build html to send email
    first_name, last_name = get_user_names(uuid_user)
    user_name = f"{first_name.title()} {last_name.title()}"
    url_s3 = f"https://s3.console.aws.amazon.com/s3/buckets/{AWS_BUCKET_NAME}?" \
             f"region={AWS_REGION}&prefix={prefix_files}/&showversions=false"
    data_email = TemplateAdminProduct.html.format(product_name=product.basic_product,
                                                  user_name=user_name,
                                                  company_name=product.company.company_name,
                                                  link=url_s3)

    send_email(subject="Review Documents - Product",
               data=data_email,
               destination=admin_emails(),
               is_html=True)


def send_email_with_template(uuid_user, type_email, render_data: dict = None):
    """
    Function to send email to seller
    :param uuid_user: uuid user to get username and email of bazar-auth
    :param type_email: type email to seller. It can be ["User-Approved", "User-Rejected", "Product-Approved",
    :param render_data: data to render
    "Product-Rejected"]
    """
    allowed_types = ['TemplateAdminUserApproved',
                     'TemplateAdminUserRejected',
                     'TemplateAdminProductApproved',
                     'TemplateAdminProductRejected',
                     'TemplateSuccessfulOrderSeller',
                     'TemplateSuccessfulOrderBuyer']

    if type_email not in allowed_types:
        current_app.logger.error(f"type email: {type_email} to seller not recognized")
        return False

    # Build html to send email
    first_name, last_name = get_user_names(uuid_user)
    seller_email = [get_email(uuid_user)]
    user_name = f"{first_name.title()} {last_name.title()}"
    if type_email == 'TemplateAdminUserApproved':
        subject = 'Review User - Approved'
        data_email = render_template(f'{type_email}.html', link_bazar=LINK_BAZAR, **render_data)
        # if you want see static template
        # with open("TemplateAdminUserApprovedSTATIC.html", "wb") as f:
        #     f.write(data_email.encode())

    elif type_email == 'TemplateAdminUserRejected':
        subject = 'Review User - Rejected'
        data_email = render_template(f'{type_email}.html', link_bazar=LINK_BAZAR, **render_data)

    elif type_email == 'TemplateAdminProductApproved':
        subject = 'Review Product - Approved'
        data_email = render_template(f'{type_email}.html', user_name=user_name, link_bazar=LINK_BAZAR)

    elif type_email == 'TemplateAdminProductRejected':
        subject = 'Review Product - Rejected'
        data_email = render_template(f'{type_email}.html', user_name=user_name, link_bazar=LINK_BAZAR, **render_data)

    elif type_email == 'TemplateSuccessfulOrderSeller':
        subject = 'Bazar sales confirmation'
        data_email = render_template(f'{type_email}.html', user_name=user_name, **render_data)

    elif type_email == 'TemplateSuccessfulOrderBuyer':
        subject = 'Bazar purchase confirmation'
        data_email = render_template(f'{type_email}.html', **render_data)

    # if you want sent email to test uncomment next line with your email
    # seller_email = ['custom@hotmail.com', 'custom@gmail.com']

    return send_email(subject=subject, data=data_email, destination=seller_email, is_html=True)


def get_field_is_like(list_objects, user_uuid):
    """
    Function to determinate if products has like
    :param list_objects: list of products
    :param user_uuid: uuid user to validate if this user liked product
    :return: list products
    """
    for p in list_objects:
        p.check_use_like(user_uuid)
    return list_objects


def get_extra_product_info(list_objects):
    """
    Function to fill data about urls files, urls images and uuid seller
    :param list_objects: list of products
    :return: list of products with extra information
    """
    list_e_objects = []
    for p in list_objects:
        p.uuid_seller = p.company.user_r.uuid
        ep = ProductEntity.from_orm(p)
        ep.url_images = list(p.url_images_ap)
        ep.url_files = [x.url for x in p.url_files_ap]
        list_e_objects.append(ep)
    return list_e_objects


def get_product_by_uuid_product(session, uuid_product):
    """
    Function to get a specific product by uuid
    :param session: session sqlalchemy
    :param uuid_product: uuid product
    :return: product
    """
    product = session.query(Product).filter_by(uuid=uuid_product).first()
    if product is None:
        e = api_error('ObjectNotFound')
        e.error['description'] = e.error['description'] + f' <product uuid_product: {uuid_product}>'
        current_app.logger.error(e.error['description'])
        abort(code=e.status_code, message=e.message, error=e.error)
    return product


def get_user_by_uuid_user(session, uuid_user):
    """
    Function to get a specific user by uuid
    :param session: session sqlalchemy
    :param uuid_user: uuid user
    :return: user
    """
    user = session.query(User).filter_by(uuid=uuid_user).first()
    if user is None:
        e = api_error('ObjectNotFound')
        e.error['description'] = e.error['description'] + f' <user uuid_user: {uuid_user}>'
        current_app.logger.error(e.error['description'])
        abort(code=e.status_code, message=e.message, error=e.error)
    return user


class UtilsDatabase:
    def __init__(self, adapter_db):
        self.session_maker = sessionmaker(bind=adapter_db.engine)
        self.session = sessionmaker(bind=adapter_db.engine, expire_on_commit=False)()

    def get_user_by_uuid_user(self, uuid_user):
        with self.session_maker() as session:
            user = session.query(User).filter_by(uuid=uuid_user).first()
            if user is None:
                e = api_error('ObjectNotFound')
                e.error['description'] = e.error['description'] + f' <user uuid_user: {uuid_user}>'
                current_app.logger.error(e.error['description'])
                abort(code=e.status_code, message=e.message, error=e.error)
            return user

    def get_company_by_uuid_user(self, uuid_user):
        with self.session_maker() as session:
            current_app.logger.info(f"Getting company by user uuid")
            user = self.get_user_by_uuid_user(uuid_user)
            company = session.query(Company).filter_by(user_id=user.id).first()
            if company is None:
                e = api_error('ObjectNotFound')
                e.error['description'] = e.error['description'] + f' <company uuid_user: {uuid_user}>'
                current_app.logger.error(e.error['description'])
                abort(code=e.status_code, message=e.message, error=e.error)
            return company

    def close_session(self):
        self.session.close()
