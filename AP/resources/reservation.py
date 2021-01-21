from flask import request, make_response, url_for, redirect, render_template
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity,jwt_required, get_current_user, jwt_optional

from models.reservation import Reservation, reservation_list
from models.user import User
from models.workspace import Workspace
from schemas.reservation import ReservationSchema

import json

reservation_schema = ReservationSchema()


class ReservationListResource(Resource):

    def put(self):

        data = request.form
        data2 = json.dumps(data)
        data3 = json.loads(data2)

        date = data3["datetime"]
        workspace = data3["workspace"]
        timeend = data3["timeend"]
        timestart = data3["timestart"]
        id = data3['id']
        reservation = Reservation.get_by_id2(id)
        reservation.reservor = data3["name"] or reservation.reservor

        reservation.workspace = Workspace.get_by_name(workspace).id or reservation.workspace

        reservation.datetime = str(date) + "T" + timestart or reservation.datetime
        reservation.datetimeend = str(date) + "T" + timeend or reservation.datetimeend

        reservation.save()

        resp = make_response(redirect(url_for('hello')))
        return resp


    def get(self):
        data = []

        for reservation in reservation_list:
            data.append(reservation.data)

        return {'data': data}, HTTPStatus.OK


    def post(self):

        data = request.form
        data2 = json.dumps(data)
        data3 = json.loads(data2)

        user = data3['user']
        data, errors = reservation_schema.load(data=data3)
        if errors:
            return  {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST

        date = data3["datetime"]
        timeend = data3["endtime"]
        timestart = data3["starttime"]

        datetime = str(date) + "T" + timestart
        datetimeend = str(date) + "T" + timeend

        news = timestart.split(":")[0]
        newe = timeend.split(":")[0]

        if news < "16" or newe > "21":
            return {'message': "Time bust be between 4pm and 9pm."}
        else:

            resp = make_response(redirect(url_for('hello')))

            reservation = Reservation(**data)
            reservation.datetime = datetime
            reservation.datetimeend = datetimeend
            reservation.reservor = user
            reservation.save()
            return resp

    def delete(self):
        data = request.args.get('jsdata')
        reservation = Reservation.get_by_id(data)

        reservation.delete()

        return render_template('deleted.html')


class ReservationResource(Resource):

    def get(self, reservation_id):
        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id), None)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        return reservation.data, HTTPStatus.OK

    def put(self, reservation_id):
        data = request.get_json()

        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id), None)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        reservation.reservor = data['reservor']
        reservation.datetime = data['datetime']
        reservation.datetimeend = data['datetimeend']
        reservation.workspace = data['workspace']

        return reservation.data, HTTPStatus.OK

    def delete(self, reservation_id):
        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id), None)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        reservation_list.remove(reservation)

        return {}, HTTPStatus.NO_CONTENT
