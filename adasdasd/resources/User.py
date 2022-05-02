from flask_restful import Resource

from .. import db
from ..models import UserModel


class UserService(Resource):

    def get_user(self, _id):
        user = db.session.query(UserModel).get_or_404(_id)
        return user.to_json()
