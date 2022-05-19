from abc import ABC, abstractmethod, ABCMeta
from typing import Mapping, TypeVar, Generic
from common.base_data import BaseData
from common.base_model import BaseModel

Model = TypeVar('Model', bound=BaseModel)
ModelData = TypeVar('ModelData', bound=BaseData)

class BaseDataSource(ABC, Generic[Model, ModelData]):

    @property
    def modelType(self):
        return self.__dict__['__orig_class__'].__dict__['__args__'][0]

    @property
    def dataModelType(self):
        return self.__dict__['__orig_class__'].__dict__['__args__'][1]

    @abstractmethod
    def get_by_id(id: str) -> Model:
        pass

    @abstractmethod
    def save(model: Model) -> Model:
        pass

    @abstractmethod
    def delete(model: Model) -> Model:
        pass

    @abstractmethod
    def create(model: Model) -> Model:
        pass