from common.models.task import Task, TaskData
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
from common.cache import cache
import json
import sys

class TaskDAO():
    def __init__(self, dbSession):
        self._db_session = dbSession

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

        if cache.exists(task_id):
            cached_data = json.loads(cache.get(task_id).decode("utf-8"))
            return Task(**cached_data)

        task: Task = None
        try:
            stmt = select(TaskData).where(TaskData.id == task_id)
            result = self._db_session.execute(stmt).scalars().one()            
            task = Task.from_orm(result)

            json_data = json.dumps(task.to_dict())
            cache.set(task_id, json_data)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
        except NoResultFound:
            print("No result found for Task UUID {0}".format(str(task_id)))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        return task

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