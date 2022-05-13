import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail


api = Api()
db = SQLAlchemy()
jwt = JWTManager()

sendmail = Mail()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    if not os.path.exists(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getenv('DATABASE_PATH') + os.getenv('DATABASE_NAME')
    db.init_app(app)

    import src.resources as resources

    api.add_resource(resources.UsersRsc, '/users')
    api.add_resource(resources.UserRsc, '/users/<id>')

    api.add_resource(resources.SensorsRsc, '/sensors')
    api.add_resource(resources.SensorRsc, '/sensors/<id>')

    api.add_resource(resources.VerifiedSeismsRsc, '/verified-seisms')
    api.add_resource(resources.VerifiedSeismRsc, '/verified-seisms/<id>')

    api.add_resource(resources.UnverifiedSeismsRsc, '/unverified-seisms')
    api.add_resource(resources.UnverifiedSeismRsc, '/unverified-seisms/<id>')

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    app.config["MAIL_HOSTNAME"] = os.getenv("MAIL_HOSTNAME")
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["FLASKY_MAIL_SENDER"] = os.getenv("FLASKY_MAIL_SENDER")

    sendmail.init_app(app)
    api.init_app(app)

    from .auth import routes
    app.register_blueprint(routes.auth)

    return app
