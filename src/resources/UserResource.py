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

        if db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None:
            return "Email already in use", 409

        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201


class UserResource(Resource):
    @staticmethod
    def get(username):
        user = db.session.query(UserModel).filter_by(username=username).first_or_404()
        return user.to_json()

    @staticmethod
    def delete(username):
        user = db.session.query(UserModel).filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        return '', 204

    @staticmethod
    def put(username):
        user = db.session.query(UserModel).filter_by(username=username).first_or_404()
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201
