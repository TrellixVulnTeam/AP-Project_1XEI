#! /usr/bin/python3.8

from flask import Flask,render_template, redirect, request, url_for, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import jwt_required, get_jwt_identity

import time
import requests

from config import Config
from extensions import db, jwt
from models.user import User
from resources.reservation import ReservationListResource, ReservationResource
from resources.workspace import WorkspaceListResource, WorkspaceResource
from resources.user import UserListResource, UserResource, MeResource, Test
from resources.token import TokenResource
from resources.refresh import TokenRefreshResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/'

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)


def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(Test, '/Test')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(ReservationListResource, '/reservations')
    api.add_resource(ReservationResource, '/reservations/<int:reservation_id>')
    api.add_resource(WorkspaceListResource, '/workspaces')
    api.add_resource(WorkspaceResource, '/workspaces/<int:workspace_id>')
    api.add_resource(TokenResource, '/token')
    api.add_resource(TokenRefreshResource, '/token/refresh')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/test')
    def testi():
        requests.get('http://localhost:5000/Test')
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def logginIn():

        return render_template('login.html')

    @app.route('/hello',  methods=['GET'])
    @jwt_required
    def hello():
        username = get_jwt_identity()
        return jsonify({'hello': 'from {}'.format(username)}), 200

    @app.route('/token', methods=['POST'])
    def token():
        return redirect(url_for('index'))

if __name__ == '__main__':
    app = create_app()
    app.run()