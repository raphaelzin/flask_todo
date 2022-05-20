import json
from typing import List
from common.models.task import Task, TaskData
from common.cache import cache
from sqlalchemy import select
from common.accessors.base_accessors.BasePersistenceDataSource import BasePersistenceDataSource as DBDataSource
from common.accessors.base_accessors.BaseCacheDataSource import BaseCacheDataSource as CacheDataSource


class TaskDAO():
    def __init__(self, dbSession, cacheSession):
        self.cacheDataSource = CacheDataSource[Task, TaskData](cacheSession)
        self.persistentDataSource = DBDataSource[Task, TaskData](dbSession)

    def get_all_tasks(self):
        return self.persistentDataSource.get_all()

    def get_task_by_uuid(self, task_id) -> Task:
        cached = self.cacheDataSource.get_by_id(task_id)
        if cached:
            return cached
        
        obj = self.persistentDataSource.get_by_id(task_id)
        self.cacheDataSource.save(obj)
        return obj
        
    def save_task(self, task: Task):
        object = self.persistentDataSource.save(task)
        if object is not None:
            self.cacheDataSource.save(object)
        else:
            self.cacheDataSource.delete(task.id)

    def delete_task(self, task_id):
        self.persistentDataSource.delete(task_id)
        self.cacheDataSource.delete(task_id)