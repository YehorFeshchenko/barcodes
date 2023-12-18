import jwt
from functools import wraps
from flask import request, jsonify, make_response
import config
from Server.models.user import User
from Server.models.base import db


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return make_response(jsonify({'message': 'Token is missing'}, 401))

        try:
            data = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
            user = db.session.query(User).filter_by(id=data['userId']).first()
        except:
            return make_response(jsonify({'message': 'Token is invalid'}, 401))
        return f(user, *args, **kwargs)
    return decorated