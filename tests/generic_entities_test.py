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

from tests.utils import validate_data_entity, validate_instance_properties_entity, get_all_entities


#
# This file contains unit-tests. It is an independent logic to the application
# @author David Córdoba
#


class TestEntity:

    def test_all_entities(self):
        if os.getcwd().split('/')[-1] == 'tests':
            from_current_file = True
        else:
            from_current_file = False
        all_entities = get_all_entities(from_current_file)
        for e in all_entities:
            print(f"Evaluating entity: {e[0].__name__}")
            parse = e[0].parse_obj(e[1])
            validate_data_entity([parse], e[0], [e[1]])
            validate_instance_properties_entity([parse], e[0])
