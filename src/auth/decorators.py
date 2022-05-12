from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(roles):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if claims['role'] in roles:
                return fn(*args, **kwargs)
            else:
                return 'Role not allowed to access this route.', 403

        return wrapper

    return decorator


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    claims = {
        'role': user.role,
        'id': user.id,
        'email': user.email
    }
    return claims
