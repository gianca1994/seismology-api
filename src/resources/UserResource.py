from flask_restful import Resource
from flask import request, jsonify
from .. import db
from src.models import UserModel


class UsersResource(Resource):
    @staticmethod
    def get():
        users = db.session.query(UserModel).all()
        return jsonify([user.to_json_short() for user in users])

    @staticmethod
    def post():
        user = UserModel.from_json(request.get_json())
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201


class UserResource(Resource):
    @staticmethod
    def get(username):
        try:
            user = db.session.query(UserModel).filter_by(username=username).first()
            return user.to_json()
        except:
            return 'The user does not exist', 404

    @staticmethod
    def delete(username):
        try:
            user = db.session.query(UserModel).filter_by(username=username).first()
            db.session.delete(user)
            db.session.commit()
            return '', 204
        except:
            return 'The user does not exist', 404

    @staticmethod
    def put(username):
        try:
            user = db.session.query(UserModel).filter_by(username=username).first()
            data = request.get_json().items()
            for key, value in data:
                setattr(user, key, value)
            db.session.add(user)
            db.session.commit()
            return user.to_json(), 201
        except:
            return 'The user does not exist', 404
