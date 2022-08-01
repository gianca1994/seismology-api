from flask import request, jsonify
from flask_restful import Resource

from .. import db
from ..auth.decorators import role_required
from ..models import SensorModel


class SensorsResource(Resource):

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get():
        page, per_page = 1, 5
        sensors = db.session.query(SensorModel)

        if request.get_json():
            filters = request.get_json().items()
            print(filters)
            for k, v in filters:
                if k == "name":
                    sensors = sensors.filter(SensorModel.name.like("%" + v + "%"))
                if k == "userId[lte]":
                    sensors = sensors.filter(SensorModel.userId <= v)
                if k == "userId[gte]":
                    sensors = sensors.filter(SensorModel.userId >= v)
                if k == "userId":
                    sensors = sensors.filter(SensorModel.userId == v)
                if k == "status":
                    sensors = sensors.filter(SensorModel.status)
                if k == "active":
                    sensors = sensors.filter(SensorModel.active)

                if k == "sort_by":
                    if k == "name":
                        sensors = sensors.order_by(SensorModel.name)
                    if v == "name.desc":
                        sensors = sensors.order_by(SensorModel.name.desc())
                    if k == "active":
                        sensors = sensors.order_by(SensorModel.active)
                    if v == "active.desc":
                        sensors = sensors.order_by(SensorModel.active.desc())
                    if k == "status":
                        sensors = sensors.order_by(SensorModel.status)
                    if v == "status.desc":
                        sensors = sensors.order_by(SensorModel.status.desc())

                if k == "page":
                    page = int(v)
                if k == "perpage":
                    per_page = int(v)

        sensors = sensors.paginate(page, per_page, True, 100)
        return jsonify({
            "Sensors": [sensor.to_json() for sensor in sensors.items],
            "total": sensors.total,
            "pages": sensors.pages,
            "page": page
        })

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def post():
        sensor = SensorModel.from_json(request.get_json())
        try:
            db.session.add(sensor)
            db.session.commit()
        except Exception as error:
            return str(error), 400
        return sensor.to_json(), 201


class SensorResource(Resource):
    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get(id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def put(id):
        sensor = db.session.query(SensorModel).get_or_404(id)

        for key, value in request.get_json().items():
            setattr(sensor, key, value)
        db.session.add(sensor)

        try:
            db.session.commit()
            return sensor.to_json(), 201

        except Exception as error:
            return str(error), 400

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def delete(id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)

        try:
            db.session.commit()
            return 'Successful deleted sensor', 204

        except Exception as error:
            db.session.rollback()
            return str(error), 400


class SensorsInfo(Resource):
    def get(self):
        sensors = db.session.query(SensorModel)
        return jsonify({"sensors": [sensor.to_json_public() for sensor in sensors]})
