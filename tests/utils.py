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
import os
import random
import string
import uuid
from datetime import timedelta, datetime, date
from importlib import import_module

import pydantic
from pydantic.main import ModelMetaclass


#
# This class lets contains generic methods to unit-tests.
# @author David Córdoba
#


def validate_instance_properties_entity(objects_parsed, e):
    if not isinstance(objects_parsed, list):
        raise Exception(f"objects_parsed is not list")
    # Validate instances
    for o in objects_parsed:
        for key in e.schema()['properties'].keys():
            if type(getattr(o, key)) != list:
                assert isinstance(type(getattr(o, key)), type(e.__fields__[key].type_))
            else:
                assert isinstance(type(getattr(o, key)), type(list))


def validate_data_entity(objects_parsed, e, data_mocks):
    if not isinstance(objects_parsed, list) or not isinstance(data_mocks, list):
        raise Exception(f"objects_parsed or data_mocks is not list")
    if len(objects_parsed) != len(data_mocks):
        raise Exception(f"len of objects_parsed must be equal to len of data_mocks")
    # Validate data
    for main_idx, o in enumerate(objects_parsed):
        for key in e.schema()['properties'].keys():
            if type(getattr(o, key)) != list:
                assert getattr(o, key) == data_mocks[main_idx].get(key)
            else:
                if len(getattr(o, key)):
                    e_instance = type(getattr(o, key)[0])
                    is_entity_pyd = type(e_instance) == ModelMetaclass
                    if not is_entity_pyd:
                        for idx, item in enumerate(getattr(o, key)):
                            assert data_mocks[main_idx].get(key)[idx] == item
                    else:
                        for idx, item in enumerate(getattr(o, key)):
                            assert getattr(o, key)[idx] == e_instance.parse_obj(data_mocks[main_idx].get(key)[idx])

                            
def get_random_string_upper_and_lower(length=5):
    result_str = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return result_str


def get_random_date(start=datetime.strptime(f'1/1/{date.today().year} 12:00 AM', '%m/%d/%Y %I:%M %p'),
                    end=datetime.strptime(f'12/31/{date.today().year} 11:59 PM', '%m/%d/%Y %I:%M %p')):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    random_date = start + timedelta(seconds=random_second)
    return random_date.date()


def get_random_dict(n=3):
    values = ['value1', 'value2']
    mydict = {"key " + str(i): values[0] for i in range(n)}
    mydict["key " + str(random.randrange(n))] = values[1]
    return mydict


def get_random_value_from_instance_type(type_f, list_sub_fields, to_example=True):
    if issubclass(type_f, uuid.UUID):
        if to_example:
            random_val = str(uuid.uuid4())
        else:
            random_val = uuid.uuid4()
    elif issubclass(type_f, pydantic.networks.AnyHttpUrl):
        random_val = f'https://example/{get_random_string_upper_and_lower()}'
    elif issubclass(type_f, date):
        if to_example:
            random_val = str(get_random_date())
        else:
            random_val = get_random_date()
    elif issubclass(type_f, str):
        random_val = get_random_string_upper_and_lower()
    elif issubclass(type_f, bool):
        random_val = random.randint(0, 1)
    elif issubclass(type_f, int):
        random_val = random.randint(0, 10)
    elif issubclass(type_f, float):
        random_val = round(random.random(), 2)
    elif issubclass(type_f, dict):
        random_val = get_random_dict()
    else:
        raise Exception(f"Not register type {type_f} to generates random data")

    if list_sub_fields:
        return [random_val]
    else:
        return random_val


def generate_data_entity(e, to_example=True):
    dict_entity = {x: e.__fields__[x].outer_type_ for x in e.__fields__}
    for field in e.__fields__:
        list_sub_fields = False
        if e.__fields__[field].sub_fields is not None:
            type_f = e.__fields__[field].sub_fields[0].outer_type_
            list_sub_fields = True

        else:
            type_f = e.__fields__[field].outer_type_

        if getattr(type_f, '__fields__', None) is not None:
            random_val = [generate_data_entity(type_f, to_example)]
        else:
            random_val = get_random_value_from_instance_type(type_f, list_sub_fields, to_example)
        dict_entity[field] = random_val
    return dict_entity


def get_all_entities(from_current_file):
    list_entity_names = []
    list_entities = []
    list_data_entities = []
    if from_current_file:
        base_dir = '../src/domain/entities/'
    else:
        base_dir = 'src/domain/entities/'
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith("_entity.py"):
                route = os.path.join(root, file)
                if from_current_file:
                    base = ".".join(route.split('/')[1:-1])
                else:
                    base = ".".join(route.split('/')[:-1])
                name = file.split('.')[0]
                imported_module = import_module(f"{base[base.find('.src.') + 1:]}.{name}")
                for attribute_name in dir(imported_module):
                    if attribute_name.endswith("Entity"):
                        if attribute_name not in list_entity_names:
                            attribute = getattr(imported_module, attribute_name)
                            entity_data = generate_data_entity(attribute, to_example=False)
                            list_entity_names.append(attribute_name)
                            list_entities.append(attribute)
                            list_data_entities.append(entity_data)
    return list(zip(list_entities, list_data_entities))
