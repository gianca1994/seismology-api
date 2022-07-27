from werkzeug.security import generate_password_hash, check_password_hash

from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(8), default="standard")
    sensors = db.relationship('Sensor', back_populates='user')

    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')

    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return 'User: %r %r %r >' % (self.email, self.firstname, self.lastname)

    def to_json(self):
        return {
            'id': str(self.id),
            'email': str(self.email),
            'firstname': str(self.firstname),
            'lastname': str(self.lastname),
            'role': str(self.role)
        }

    def to_json_short(self):
        return {
            'id': str(self.id),
            'email': str(self.email),
            'firstname': str(self.firstname),
            'lastname': str(self.lastname)
        }

    @staticmethod
    def from_json(user_json):
        return User(
            email=user_json.get('email'),
            plain_password=user_json.get('password'),
            firstname=user_json.get('firstname'),
            lastname=user_json.get('lastname'),
            role=user_json.get('role')
        )
