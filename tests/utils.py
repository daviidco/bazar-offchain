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
