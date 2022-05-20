import json
from typing import Generic
from common.accessors.base_accessors.BaseDataSource import Model, ModelData, BaseDataSource

class BaseCacheDataSource(BaseDataSource[Model, ModelData], Generic[Model, ModelData]):
    
    def __init__(self, cacheSession):
        self._cache_session = cacheSession

    def get_by_id(self, id: str) -> Model:
        if not self._cache_session.exists(id):
            return None

        cached_data = json.loads(self._cache_session.get(id).decode("utf-8"))
        return self.modelType(**cached_data)

    def save(self, model: Model) -> Model:
        json_data = json.dumps(model.to_dict())
        return self._cache_session.set(model.id, json_data)

    def delete(self, id) -> Model:
        self._cache_session.delete(id)

    def create(self, model: Model) -> Model:
        self.save(model)

    def cache(self, key, value):
        self._cache_session.set(key, value)