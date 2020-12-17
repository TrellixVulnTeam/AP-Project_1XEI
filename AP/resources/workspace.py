from flask import request, jsonify
from flask_restful import Resource
from http import HTTPStatus

import json
from models.workspace import Workspace, workspace_list
from flask_marshmallow import Marshmallow


class WorkspaceListResource(Resource):

    def get(self):
        data = []

        for workspace in workspace_list:
            data.append(workspace.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        name = data.get('name')

        workspace = Workspace (
            name=name
        )
        workspace.save()

        data = {
            'name':  workspace.name
        }

        return data, HTTPStatus.CREATED



class WorkspaceResource(Resource):

    def get(self, name):

        workspace = Workspace.get_by_name(name=name)

        data = {
            'name': workspace.name
        }

        return data, HTTPStatus.OK

    def put(self, workspace_id):
        data = request.get_json()

        workspace = next((workspace for workspace in workspace_list if workspace.id == workspace_id), None)

        if workspace is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        workspace.id = data['id']
        workspace.name = data['name']

        return workspace.data, HTTPStatus.OK

    def delete(self, workspace_id):
        workspace = next((workspace for workspace in workspace_list if workspace.id == workspace_id), None)

        if workspace is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        workspace_list.remove(workspace)

        return {}, HTTPStatus.NO_CONTENT


class AllWorkspaces(Resource):

    def get(self):

        data = Workspace.get_all()

        print(data)

        return data
