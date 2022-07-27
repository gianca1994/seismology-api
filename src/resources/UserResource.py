from flask_restful import Resource
from flask import request, jsonify
from .. import db
from src.models import UserModel
from ..auth.decorators import role_required


class UsersResource(Resource):

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get():
        users = db.session.query(UserModel).all()
        return jsonify({"Users": [user.to_json() for user in users]})


class UserResource(Resource):
    @staticmethod
    @role_required(roles=["standard", "admin"])
    def get(id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def delete(id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    @staticmethod
    @role_required(roles=["standard", "admin"])
    def put(id):
        user = db.session.query(UserModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201


class UsersInfo(Resource):
    def get(self):
        users = db.session.query(UserModel)
        return jsonify({"Users": [user.to_json_short() for user in users]})