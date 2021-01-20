#! /usr/bin/python3.8

from flask import Flask,render_template, redirect, request, url_for, jsonify, json,make_response
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies, unset_access_cookies, unset_refresh_cookies

import time
import requests

from config import Config
from extensions import db, jwt
from models.user import User
from resources.reservation import ReservationListResource, ReservationResource
from resources.workspace import WorkspaceListResource, WorkspaceResource, AllWorkspaces
from resources.user import UserListResource, UserResource, MeResource, Test, User2Resource
from resources.token import TokenResource
from resources.refresh import TokenRefreshResource
from flask_marshmallow import Marshmallow
from models.workspace import Workspace
from models.reservation import Reservation
from models.user import User


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
    api.add_resource(User2Resource, '/users2')
    api.add_resource(Test, '/Test')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(ReservationListResource, '/reservations')
    api.add_resource(ReservationResource, '/reservations/<int:reservation_id>')
    api.add_resource(WorkspaceListResource, '/workspaces')
    api.add_resource(AllWorkspaces, '/allworkspaces')
    api.add_resource(WorkspaceResource, '/workspaces/<string:name>')
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

    @app.route('/register', methods=['GET', 'POST'])
    def register():

        return render_template('register.html')

    @app.route('/hello',  methods=['GET'])
    @jwt_required
    def hello():
        users = []
        workspaces= Workspace.query.all()
        user = get_jwt_identity()
        userid = User.get_by_username(user).id
        users.append(userid)
        reservations = Reservation.query.filter_by(reservor=userid).all()
        reser = []
        for reservation in reservations:
            try:
                ids = reservation.workspace
                a = Workspace.get_by_id(ids)
                reservation.name = a.name
                reser.append(reservation)
            except:
                print("rip")
        resp = make_response(render_template('reservations.html', reservations=reservations, workspaces=workspaces, users=users ))
        return resp

    @app.route('/dashboard', methods=['GET'])
    @jwt_required
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/registrationform', methods=['GET'])
    @jwt_required
    def registrationform():
        return render_template('registrationform.html')

    @app.route('/editReservation/<int:id>/', methods=['GET'])
    @jwt_required
    def editReservation(id):
        workspaces = Workspace.query.all()
        return render_template('editReservation.html', workspaces=workspaces, id=id)

    @app.route('/token', methods=['POST'])
    def token():
        return redirect(url_for('index'))

    @app.route('/logout', methods=['POST'])
    def logout():
        resp = jsonify({'logout': True})
        unset_access_cookies(resp)
        unset_refresh_cookies(resp)
        unset_jwt_cookies(resp)
        return redirect(url_for('hello'))

    @app.route('/check', methods=['GET'])
    def check():
        data = request.args.get('jsdata')
        space = request.args.get('space')
        check_list = []
        reservations = Reservation.query.all()
        spaceid = Workspace.get_by_name(space).id
        print(spaceid)
        for reservation in reservations:
            if spaceid == reservation.workspace:
                newdate = str(reservation.datetime).split(" ")[0]
                if newdate == data:
                    d = str(reservation.datetime)
                    d2 = str(reservation.datetimeend)
                    date3 = d + " - " + d2
                    check_list.append(date3)
        if not reservations:
            check_list.append("No reservations")

        return render_template('reservationscheck.html', checklist=check_list)

    @app.route('/admin',  methods=['GET'])
    @jwt_required
    def admin():
        username = get_jwt_identity()
        user = User.get_by_username(username)
        if user.is_admin:
            workspaces = Workspace.query.all()
            reservations = Reservation.query.all()
            reser = []
            i = 0
            for reservation in reservations:
                try:
                    ids = reservation.workspace
                    ids2 = reservation.reservor
                    a = Workspace.get_by_id(ids)
                    b = User.get_by_id(ids2)
                    reservation.correct_user = b.name
                    reservation.name = a.name
                    reser.append(reservation)
                except:
                    print("rip")
            clients = User.query.all()
            return render_template('admin.html', reservations=reservations, workspaces=workspaces, clients=clients)
        else:
            return render_template('notadmin.html')

    @app.route('/deleteworkspace', methods=['GET'])
    def deleteworkspace():
        data = request.args.get('jsdata')
        workspace = Workspace.get_by_id(data)

        workspace.delete()

        return render_template('deleted.html')

    @app.route('/deletereservation', methods=['GET'])
    def deletereservation():
        data = request.args.get('jsdata')
        reservation = Reservation.get_by_id(data)
        print(data)

        reservation.delete()

        return render_template('deleted.html')

    @app.route('/deleteuser', methods=['GET'])
    def deleteuser():
        data = request.args.get('jsdata')
        user = User.get_by_id(data)

        user.delete()

        return render_template('deleted.html')
if __name__ == '__main__':
    app = create_app()
    app.run()