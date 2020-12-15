from extensions import db

reservation_list = []


def get_last_id():
    if reservation_list:
        last_reservation = reservation_list[-1]
    else:
        return 1


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    reservor = db.Column(db.Integer())
    datetime = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    workspace = db.Column(db.Integer())
