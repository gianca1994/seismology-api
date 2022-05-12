from .. import db


class Seism(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column("datetime", db.DateTime, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String(99), nullable=False)
    longitude = db.Column(db.String(99), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)

    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete='RESTRICT'), nullable=False)
    sensor = db.relationship('Sensor', back_populates='seisms', uselist=False, single_parent=True)
