from abc import ABC, abstractmethod


class IStorage(ABC):

    @abstractmethod
    def copy_object(self, origin_key: str, destination_key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def get_object(self, key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def key_existing_size__list(self, key):
        """return the key's size if it exist, else None"""
        raise Exception('Not implemented method')

    @abstractmethod
    def upload_file(self, filename: str, key: str):
        raise Exception('Not implemented method')

    @abstractmethod
    def put_object(self, body: any, key: str, content_type: str, bucket: str = None):
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