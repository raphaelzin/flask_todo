from common.models.task import Task, TaskData
from sqlalchemy import select
from sqlalchemy.orm.exc import NoResultFound
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
        task: Task = None
        try:
            stmt = select(TaskData).where(TaskData.id == task_id)
            result = self._db_session.execute(stmt).scalars().one()
            task = Task.from_orm(result)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
        except NoResultFound:
            print("No result found for Task UUID {0}".format(str(task_id)))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
        return task

    def save_task(self, task: Task):
        if task.id is not None:
            # update
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
        pass

    def _update_task(self, task_data):
        stmt = select(TaskData).where(TaskData.id == task_data.id)
        result = self._db_session.execute(stmt).scalars().one()
        result.update(task_data)
        self._db_session.commit()
        pass

    def _create_task(self, task_data: TaskData):
        self._db_session.add(task_data)
        self._db_session.commit()
        pass