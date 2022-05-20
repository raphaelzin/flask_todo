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
        tasks: List[Task] = []

        try:
            stmt = select(TaskData)
            for row in self._db_session.execute(stmt).scalars():
                tasks.append(Task.from_orm(row))
        except ValueError as e:
            print(f"Error: {e}")
        return tasks

    def get_task_by_uuid(self, task_id) -> Task:
        cached = self.cacheDataSource.get_by_id(task_id)
        if cached:
            return cached
        
        obj = self.persistentDataSource.get_by_id(task_id)
        self.cacheDataSource.save(obj)
        return obj
        
    def save_task(self, task: Task):
        object = self.persistentDataSource.save(task)
        if object:
            self.cacheDataSource.save(object)

    def delete_task(self, task_id):
        self.persistentDataSource.delete(task_id)
        self.cacheDataSource.delete(task_id)