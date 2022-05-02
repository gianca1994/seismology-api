from flask import request, jsonify
from flask_restful import Resource

from .. import db
from ..models import SensorModel


class SensorsResource(Resource):
    @staticmethod
    def get():
        sensors = db.session.query(SensorModel).all()
        return jsonify([sensor.to_json_public() for sensor in sensors])

    @staticmethod
    def post():
        sensor = SensorModel.from_json(request.get_json())

        try:
            db.session.add(sensor)
            db.session.commit()
            return sensor.to_json(), 201

        except Exception as error:
            return str(error), 400


class SensorResource(Resource):
    @staticmethod
    def get(id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        return sensor.to_json()

    @staticmethod
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
    def delete(id):
        sensor = db.session.query(SensorModel).get_or_404(id)
        db.session.delete(sensor)

        try:
            db.session.commit()
            return 'Successful deleted sensor', 204

        except Exception as error:
            db.session.rollback()
            return str(error), 400
