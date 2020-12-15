#! /usr/bin/python3.8

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from models.user import User
from resources.reservation import ReservationListResource, ReservationResource
from resources.workspace import WorkspaceListResource, WorkspaceResource
from resources.user import UserListResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(ReservationListResource, '/reservations')
    api.add_resource(ReservationResource, '/reservations/<int:reservation_id>')
    api.add_resource(WorkspaceListResource, '/workspaces')
    api.add_resource(WorkspaceResource, '/workspaces/<int:workspace_id>')


if __name__ == '__main__':
    app = create_app()
    app.run()