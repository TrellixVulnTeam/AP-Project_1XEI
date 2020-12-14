from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.reservation import Reservation, reservation_list


class ReservationListResource(Resource):

    def get(self):
        data = []

        for reservation in reservation_list:
            data.append(reservation.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        reservation = Reservation(reservor=data['reservor'],
                                  datetime=data['datetime'],
                                  workspace=data['workspace'])

        reservation_list.append(reservation)

        return reservation.data, HTTPStatus.CREATED


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
        reservation.workspace = data['workspace']

        return reservation.data, HTTPStatus.OK

    def delete(self, reservation_id):
        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id), None)

        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND

        reservation_list.remove(reservation)

        return {}, HTTPStatus.NO_CONTENT
