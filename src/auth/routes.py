from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from ..models import UserModel
from .decorators import role_required
from .. import db
from ..mail.sender_mail import send_mail

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login', methods=['POST'])
def login():

    user = (
        db.session.query(UserModel)
            .filter(UserModel.email == request.get_json().get("email"))
            .first_or_404()
    )

    if user.validate_pass(request.get_json().get('password')):
        access_token = create_access_token(identity=user)
        return {'id': str(user.id), 'email': user.email, 'role': user.role, 'access_token': access_token}, 200
    else:
        return 'Incorrect password', 401


@auth.route('/register', methods=['POST'])
@role_required(roles=["admin"])
def register():
    user = UserModel.from_json(request.get_json())
    exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None

    if exists:
        return 'Duplicated mail', 409

    try:
        send_mail(user.email, "Welcome seismology!", 'register', user=user, password=request.get_json().get('password'))

        db.session.add(user)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return str(error), 409
    return user.to_json_short(), 201
