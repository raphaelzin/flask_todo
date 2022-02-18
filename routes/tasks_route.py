from flask import jsonify, request, Blueprint
from common.models.task import Task
from common.accessors.task_dao import TaskDAO as TaskDB
from common.database import get_session

tasks_route = Blueprint('tasks_route', __name__)

@tasks_route.route('/tasks/<task_id>', methods = ['GET', 'DELETE', 'PUT'])
def task(task_id):
    session = get_session()
    taskDB = TaskDB(session)

    if request.method == "GET":
        taskdata = taskDB.get_task_by_uuid(task_id)
        if taskdata is not None:
            return jsonify(taskdata.to_dict())
        else:
            return f"Searched for task with id: {task_id}, no match!", 404

    if request.method == "PUT":
        if 'id' not in request.json:
            return "Request's body missing ID", 400
        id = request.json["id"]
        if id is None or id != task_id:
            return "request's body's ID doesn't match url's id", 400

        task = Task(**request.json)
        taskDB.save_task(task)
        return task.to_dict()
        
    if request.method == "DELETE":
        taskdata = taskDB._delete_task(task_id)
        return f"Task {task_id} Deleted"
    return

@tasks_route.route('/tasks', methods = ['POST'])
def create_task():
    session = get_session()
    if request.method == "POST":
        taskDB = TaskDB(session)
        task = Task(**request.json)
        taskDB.save_task(task)
        return task.to_dict()

@tasks_route.route('/tasks/', methods = ['GET'])
def tasks():
    session = get_session()
    taskDB = TaskDB(session)
    tasks = taskDB.get_all_tasks()
    dictTasks = list(map(lambda x: x.to_dict(), tasks))
    return jsonify(dictTasks)