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
from datetime import datetime


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
    schema = c_e.schema()
    for key in list(schema['properties'].keys()):
        """function return json help"""
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
