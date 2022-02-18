from common.models.tag import Tag
from flask import Flask, jsonify, request

app = Flask(__name__)

from routes.tasks_route import tasks_route
from common.database import get_session
from common.models.tag import Tag

app.register_blueprint(tasks_route)

# @app.after_request
# def after_request(response):
#     print(f"after_request is running! {response.status}-")
#     wrapper = {
#         "data": response.json
#     }

#     response.json = wrapper
#     return response

@app.route("/createtag", methods = ["GET"])
def createTag():
    name = request.args.get("tag_name")
    if name is None:
        return "no name given", 400

    data = Tag(title=str(name))
    session = get_session()
    session.add(data.to_data())
    session.commit()
    return jsonify(data.to_dict())

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')