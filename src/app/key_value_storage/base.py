from abc import ABC, abstractmethod


class BaseKeyValueStorage(ABC):
    @abstractmethod
    def hget_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def hset_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def hdel_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def hget_all_values(self, *args, **kwargs):
        pass

    @abstractmethod
    def hexists(self, *args, **kwargs):
        pass
