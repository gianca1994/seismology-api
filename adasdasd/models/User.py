from .. import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)

    def __repr__(self) -> str:
        return 'User: %r %r ' % (self.username, self.email)

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': str(self.email),
            'admin': self.admin
        }

    def from_json(self) -> object:
        return User(
            id=self.get('id'),
            username=self.get('username'),
            plain_password=self.get('password'),
            email=self.get('email'),
            admin=self.get('admin')
        )

    def to_json_public(self) -> dict:
        return {
            'username': self.username,
            'email': str(self.email)
        }
