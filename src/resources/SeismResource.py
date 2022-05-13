import time
from random import uniform, randint

from flask_restful import Resource

from .. import db
from ..auth.decorators import role_required
from ..models import SeismModel, SensorModel
from flask import request, jsonify


class VerifiedSeisms(Resource):

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get():
        page, per_page = 1, 5
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == True)

        if request.get_json():
            filter = request.get_json().items()

            for k, v in filter:
                if k == 'datetime':
                    seisms = seisms.filter(SeismModel.datetime == v)
                if k == 'datetimeFrom':
                    seisms = seisms.filter(SeismModel.datetime >= v)
                if k == 'datetimeTo':
                    seisms = seisms.filter(SeismModel.datetime <= v)
                if k == 'sensorId':
                    seisms = seisms.filter(SeismModel.sensorId == v)
                if k == 'magnitudeMax':
                    seisms = seisms.filter(SeismModel.magnitude <= v)
                if k == 'magnitudeMin':
                    seisms = seisms.filter(SeismModel.magnitude == v)
                if k == 'sensor.name':
                    seisms = seisms.join(SeismModel.sensor).filter(SensorModel.name.like('%' + v + '%'))

                if k == 'shortby':
                    if v == 'datetime':
                        seisms = seisms.order_by(SeismModel.dt)
                    if v == 'datime.desc':
                        seisms = seisms.order_by(SeismModel.dt.desc())
                    if v == 'sensor.name':
                        seisms = seisms.join(SeismModel.sensor).orderby(SensorModel.name)
                    if v == 'sensor.namedesc':
                        seisms = seisms.join(SeismModel.sensor).orderby(SensorModel.name.desc())

                if k == 'page':
                    page = int(v)
                if k == 'per_page':
                    per_page = int(v)

        seisms = seisms.paginate(page, per_page, True, 100)

        return jsonify({
            'Verified-seisms': [seism.to_json() for seism in seisms.items],
            'total': seisms.total,
            'pages': seisms.pages,
            'page': page
        })


class UnverifiedSeisms(Resource):

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get():
        page, per_page = 1, 5
        seisms = db.session.query(SeismModel).filter(SeismModel.verified == False)

        if request.get_json():
            filters = request.get_json().items()

            for k, v in filters:
                if 'datetime' in filters:
                    seisms = seisms.filter(SeismModel.datetime == v)
                if k == 'datetimeFrom':
                    seisms = seisms.filter(SeismModel.datetime >= v)
                if k == 'datetimeTo':
                    seisms = seisms.filter(SeismModel.datetime <= v)
                if k == 'sensorId':
                    seisms = seisms.filter(SeismModel.sensorId == v)
                if k == 'magnitude':
                    seisms = seisms.filter(SeismModel.magnitude == v)
                if k == 'depth':
                    seisms = seisms.filter(SeismModel.depth == v)

                if k == 'sort_by':
                    if v == 'datetime':
                        seisms = seisms.order_by(SeismModel.datetime)
                    if v == 'datetime.desc':
                        seisms = seisms.order_by(SeismModel.datetime.desc())
                    if v == 'sensorname':
                        seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.asc())
                    if v == 'sensorname.desc':
                        seisms = seisms.join(SeismModel.sensor).order_by(SensorModel.name.desc())

                    if v == 'magnitude':
                        seisms = seisms.order_by(SeismModel.magnitude.asc())
                    if v == 'magnitude.desc':
                        seisms = seisms.order_by(SeismModel.magnitude.desc())
                    if v == 'depth':
                        seisms = seisms.order_by(SeismModel.depth.asc())
                    if v == 'depth.desc':
                        seisms = seisms.order_by(SeismModel.depth.desc())

                    if k == 'page':
                        page = int(v)
                    if k == 'per_page':
                        per_page = int(v)

        seisms = seisms.paginate(page, per_page, True, 100)

        return jsonify({
            'Unverif-seisms': [seism.to_json() for seism in seisms.items],
            'total': seisms.total,
            'pages': seisms.pages,
            'page': page
        })

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def post():
        sensors = db.session.query(SensorModel).all()
        sensor_list = [(int(sensor.id)) for sensor in sensors]

        if sensor_list:
            value_sensor = {
                'datetime': time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime()),
                'depth': randint(5, 250),
                'magnitude': round(uniform(2.0, 5.5), 1),
                'latitude': uniform(-180, 180),
                'longitude': uniform(-90, 90),
                'verified': False,
                'sensorId': sensor_list[randint(0, len(sensor_list) - 1)]
            }

            seism = SeismModel.from_json(value_sensor)
            db.session.add(seism)
            db.session.commit()

        else:
            return 'Sensors not found, cant create seism', 400
        return seism.to_json(), 201


class VerifiedSeism(Resource):
    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get(id):
        seism = db.session.query(SeismModel).get_or_404(id)
        return seism.to_json() if seism.verified else 'Access denied', 403


class UnverifiedSeism(Resource):
    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get(id):
        seism = db.session.query(SeismModel).get_or_404(id)
        return seism.to_json() if not seism.verified else 'Access denied', 403

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def put(id):
        seism = db.session.query(SeismModel).get_or_404(id)
        data = request.get_json().items()
        if not seism.verified:
            for k, v in data:
                setattr(seism, k, v)
            try:
                db.session.add(seism)
                db.session.commit()
                return seism.to_json(), 201
            except Exception as error:
                return str(error), 400
        else:
            return 'Access denied', 403

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def delete(id):
        seism = db.session.query(SeismModel).get_or_404(id)
        if not seism.verified:
            db.session.delete(seism)
            db.session.commit()
            return 'Unverif seism delete', 204
        else:
            return 'Access denied', 403
