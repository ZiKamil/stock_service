from flask import Flask, jsonify, request
from flask_migrate import Migrate
from pydantic import BaseSettings
from models import *


app = Flask(__name__)

import routes

app.config["SECRET_KEY"] = "2d9a527e31204f93b5138a2b889f285d"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@postgres:5432/postgres"
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
