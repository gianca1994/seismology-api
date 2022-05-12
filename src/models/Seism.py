from .. import db
from .Sensor import Sensor as SensorModel
from datetime import datetime as dt


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

    def __repr__(self):
        return '<Seism: %r %r %r %r >' % (self.magnitude, self.latitude, self.longitude, self.depth)

    def to_json(self):
        self.sensor = db.session.query(SensorModel).get_or_404(self.sensorId)

        return {
            'id': self.id,
            'datetime': self.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            'magnitude': str(self.magnitude),
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'depth': self.depth,
            'verified': self.verified,
            'sensorId': self.sensorId,
            'sensor': self.sensor.to_json()
        }

    @staticmethod
    def from_json(seism_json):
        return Seism(
            id=get('id'),
            datetime=dt.strptime(get(
                'datetime'), "%Y-%m-%d %H:%M:%S"),
            magnitude=get('magnitude'),
            latitude=get('latitude'),
            longitude=get('longitude'),
            depth=get('depth'),
            verified=get('verified'),
            sensorId=get('sensorId')
        )
