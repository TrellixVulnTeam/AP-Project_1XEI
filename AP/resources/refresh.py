from http import HTTPStatus
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_jwt_identity

from utils import check_password
from models.user import User


class TokenRefreshResource(Resource):
    def post(self):

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)

        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)
        return resp, 200