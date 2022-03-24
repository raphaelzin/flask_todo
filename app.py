from flask import Flask

from routes.tasks_route import tasks_route

app = Flask(__name__)

app.register_blueprint(tasks_route)

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0')