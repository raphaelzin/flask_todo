from common.models.task import Task, TaskData

from common.cache import cache
import json
from sqlalchemy import select
from common.accessors.BasePersistenceDataSource import BasePersistenceDataSource as DBDataSource
from common.accessors.BaseCacheDataSource import BaseCacheDataSource as CacheDataSource


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
        self.cacheDataSource.cache(task_id, json.dumps(obj.to_dict()))
        return obj
        
    def save_task(self, task: Task):
        if task.id is not None:
            try:
                self._update_task(task)
            except Exception as e:
                raise e
        else:
            # create
            try:
                self._create_task(task.to_data())
            except Exception as e:
                raise e

    def _delete_task(self, task_id):
        stmt = select(TaskData).where(TaskData.id == task_id)
        result = self._db_session.execute(stmt).scalars().one()
        self._db_session.delete(result)
        self._db_session.commit()
        
        cache.delete(task_id)
        pass

    def _update_task(self, task_data):
        stmt = select(TaskData).where(TaskData.id == task_data.id)
        result = self._db_session.execute(stmt).scalars().one()
        result.update(task_data)
        self._db_session.commit()

        json_data = json.dumps(Task.from_orm(result).to_dict())
        cache.set(task_data.id, json_data)
        pass

    def _create_task(self, task_data: TaskData):
        self._db_session.add(task_data)
        self._db_session.commit()
        
        json_data = json.dumps(Task.from_orm(task_data).to_dict())
        cache.set(task_data.id, json_data)
        pass