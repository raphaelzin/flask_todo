import json
from typing import Generic
from common.accessors.BaseDataSource import Model, ModelData, BaseDataSource

class BaseCacheDataSource(BaseDataSource[Model, ModelData], Generic[Model, ModelData]):
    
    def __init__(self, cacheSession):
        self.cacheSession = cacheSession

    def get_by_id(self, id: str) -> Model:
        if not self.cacheSession.exists(id):
            return None

        cached_data = json.loads(self.cacheSession.get(id).decode("utf-8"))
        return self.modelType(**cached_data)

    def save(self, model: Model) -> Model:
        # TODO: Add to_dict and id to BaseModel
        json_data = json.dumps(model.to_dict())
        return self.cacheSession.set(model.id, json_data)

    def delete(self, model: Model) -> Model:
        self.cacheSession.delete(model.id)

    def create(self, model: Model) -> Model:
        self.save(model)

    def cache(self, key, value):
        self.cacheSession.set(key, value)