from flask import request
from flask_restful import Resource
from http import HTTPStatus

from utils import hash_password
from models.user import User


class UserListResource(Resource):
    def post(self):
        data = request.get_json('username')

        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        non_hash_pass = data.get('password')

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

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        return data, HTTPStatus.CREATED
