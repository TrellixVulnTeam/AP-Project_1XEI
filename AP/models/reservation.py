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
    datetimeend = db.Column(db.DateTime(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    workspace = db.Column(db.Integer())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_reservor(cls, reservor):
        return cls.query.filter_by(reservor=reservor).first()

    @classmethod
    def get_by_id(cls, id):
        newid = id.split("}")[0]
        return cls.query.filter_by(id=newid).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()