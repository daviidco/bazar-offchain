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
import copy
import json
import uuid
from datetime import datetime

from flask import current_app
from flask_restx import abort

from src.infrastructure.adapters.flask.app.utils.error_handling import api_error


#
# This file contains global methods
# @author David Córdoba
#
def get_date():
    return datetime.datetime.now()


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """function to check file extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Swagger Documentation
def get_help_schema(c_e):
    """function return json help"""
    schema = copy.deepcopy(c_e.schema())
    for key in list(schema['properties'].keys()):
        schema["properties"][key] = schema["properties"][key]['type']
    return json.dumps(schema["properties"], indent=2)


def get_schema(c_e):
    """function return schema with fields required"""
    schema = c_e.schema()['properties']
    internal_models = [c_e.__fields__[prop] for prop in c_e.__fields__]
    list_dicts = [{im.name: {'title': im.name, 'required': im.required}} for im in internal_models]
    dict_merged = {k: v for d in list_dicts for k, v in d.items()}
    for prop in schema:
        schema[prop]['required'] = dict_merged[prop]['required']
    return schema


def is_valid_uuid_input(uuid_to_validate) -> bool:
    try:
        uuid.UUID(str(uuid_to_validate))
        return True
    except Exception as e:
        e = api_error('UuidError')
        e.error['description'] = e.error['description'] + f' <uuid> {uuid_to_validate}'
        current_app.logger.error(f"{e.error['description']}")
        abort(code=e.status_code, message=e.message, error=e.error)


def compare_nums(num1, num2, operator='=') -> bool:
    try:
        if operator == '<':
            if num1 < num2:
                return True
        elif operator == '>':
            if num1 > num2:
                return True
        elif operator == '=':
            if num1 == num2:
                return True
        elif operator == '<=':
            if num1 <= num2:
                return True
        elif operator == '>=':
            if num1 >= num2:
                return True
        else:
            raise Exception(f'Operator {operator} not recognized')
        raise Exception(f'Compare of nums is invalid')
    except Exception as e:
        e = api_error('UndefendedError')
        e.error['description'] = f'{num1} must be {operator} than {num2}'
        current_app.logger.error(f"{e.error['description']}")
        abort(code=e.status_code, message=e.message, error=e.error)

