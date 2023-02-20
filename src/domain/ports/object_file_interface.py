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

from abc import ABC, abstractmethod


#
# This interface or port lets define the methods to implement by S3Repository.
# @author David Córdoba
#
class IStorage(ABC):

    @abstractmethod
    def copy_object(self, origin_key: str, destination_key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def get_object(self, key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def key_existing_size__list(self, key):
        raise Exception('Not implemented method')

    @abstractmethod
    def upload_file(self, filename: str, key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def put_object(self, body: any, key: str, content_type: str, bucket: str = None):
        raise Exception('Not implemented method')

    @abstractmethod
    def put_list_object(self, files: list, prefix: str, bucket: str = None):
        raise Exception('Not implemented method')

    @abstractmethod
    def file_exists(self, file_key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def update_file(self, actual_file_key: str, new_file_key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def delete_file(self, file_key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def upload_file_obj(self, buffer):
        raise Exception('Not implemented method')
