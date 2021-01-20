from flask import request, make_response, url_for, redirect
from flask_restful import Resource
from http import HTTPStatus

from utils import hash_password
from models.user import User

from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from schemas.user import UserSchema

import json

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))

class UserListResource(Resource):
    def post(self):
        data = request.form
        data2 = json.dumps(data)
        data3 = json.loads(data2)

        schemadata = user_schema.load(data=data3)

        username = data3['username']
        name = data3['name']
        email = data3['email']
        non_hash_pass = data3['password']

        if User.get_by_username(username):
            return {'message':  'Username already exists'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'Email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_pass)

        user = User(**data)

        user.save()

        resp = make_response(redirect(url_for('logginIn')))
        return resp

    def put(self, id):
        data = request.get_json()

        user = User.get_by_id(id)

        user.username = data['username']
        user.name = data['name']
        user.email = data['email']
        user.password = user.password

        user.save()


class User2Resource(Resource):
    def post(self):
        data = request.form
        data2 = json.dumps(data)
        data3 = json.loads(data2)

        username = data3['username']
        name = data3['name']
        email = data3['email']
        non_hash_pass = data3['password']

        if User.get_by_username(username):
            return {'message':  'Username already exists'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message': 'Email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_pass)

        user = User(
            username=username,
            name=name,
            email=email,
            password=password
        )

        user.save()

        resp = make_response(redirect(url_for('admin')))
        return resp

class UserResource(Resource):
    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:
            return{'message':'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK


class MeResource(Resource):

    @jwt_required
    def get(self):

        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dump(user).data, HTTPStatus.OK


class Test(Resource):
    def get(self):

        data = {
            'shit': 'works'
        }

        return data, HTTPStatus.OK