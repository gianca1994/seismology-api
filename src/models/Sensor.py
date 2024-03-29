from .. import db
from .User import User as UserModel


class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(99), nullable=False, unique=True)
    ip = db.Column(db.String(99), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    user = db.relationship('User', back_populates='sensors', uselist=False, single_parent=True)
    seisms = db.relationship('Seism', back_populates='sensor', passive_deletes='all')

    def __repr__(self):
        return '<Sensor: %r %r %r >' % (self.name, self.ip, self.port)

    def to_json(self):
        self.user = db.session.query(UserModel).get(self.userId)

        sensor_json = {
            'id': self.id,
            'name': self.name,
            'ip': self.ip,
            'port': self.port,
            'status': self.status,
            'active': self.active,
        }

        try:
           sensor_json['user'] = self.user.to_json()
        except:
            sensor_json['userId'] = self.userId
        return sensor_json

    @staticmethod
    def from_json(sensor_json):
        return Sensor(
            id=sensor_json.get("id"),
            name=sensor_json.get('name'),
            ip=sensor_json.get('ip'),
            port=sensor_json.get('port'),
            status=sensor_json.get('status'),
            active=sensor_json.get('active'),
            userId=sensor_json.get('userId')
        )

    def to_json_public(self):
        return {
            'id': self.id,
            'name': str(self.name),
            'status': self.status,
            'active': self.active
        }
