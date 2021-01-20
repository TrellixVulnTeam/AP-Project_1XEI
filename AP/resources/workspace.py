from flask import request, jsonify, make_response, url_for, redirect, render_template
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
        data = request.form
        data2 = json.dumps(data)
        data3 = json.loads(data2)

        name = data3.get('name')
        people = data3.get('people')

        workspaces = Workspace.get_all()
        check = False

        for workspace in workspaces:
            if workspace.name == name:
                check = True

        if not check:
            workspace = Workspace(
                name=name,
                size=people
            )
            workspace.save()

            resp = make_response(redirect(url_for('admin')))

            return resp
        else:
            resp = make_response(redirect(url_for('admin')))

            return resp

    def delete(self):
        data = request.args.get('jsdata')
        print(data)
        workspace = Workspace.get_by_id(data)

        workspace.delete()

        return render_template('deleted.html')


class WorkspaceResource(Resource):

    def get(self, name):

        workspace = Workspace.get_by_name(name=name)

        data = {
            'name': workspace.name,
            'size': workspace.size
        }

        return data, HTTPStatus.OK

    def put(self, workspace_id):
        data = request.get_json()

        workspace = next((workspace for workspace in workspace_list if workspace.id == workspace_id), None)

        if workspace is None:
            return {'message': 'Workspace not found'}, HTTPStatus.NOT_FOUND

        workspace.id = data['id']
        workspace.name = data['name']
        workspace.size = data['size']

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
