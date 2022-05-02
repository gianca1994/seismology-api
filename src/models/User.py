from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'User: %r %r %r %r >' % (self.username, self.email, self.firstname, self.lastname)

    def to_json(self):
        return {
            'username': str(self.username),
            'email': str(self.email),
            'firstname': str(self.firstname),
            'lastname': str(self.lastname)
        }

    def to_json_short(self):
        return {
            'username': str(self.username),
            'firstname': str(self.firstname),
            'lastname': str(self.lastname)
        }

    @staticmethod
    def from_json(user_json):
        return User(
            username=user_json.get('username'),
            password=user_json.get('password'),
            email=user_json.get('email'),
            firstname=user_json.get('firstname'),
            lastname=user_json.get('lastname'),
        )
