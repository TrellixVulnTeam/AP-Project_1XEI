from http import HTTPStatus
from flask import request, jsonify, make_response, redirect, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies

from utils import check_password
from models.user import User
import json

class TokenResource(Resource):
    def post(self):

        data = request.form
        data2 = json.dumps(data)
        data3 = json.loads(data2)
        email = data3["email"]
        password = data3["password"]

        user = User.get_by_email(email=email)

        if not user or not check_password(password, user.password):
            return {'message': 'Email or password is incorrect'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        resp = make_response(redirect(url_for('hello')))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp
