import os
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from models import *

def require_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            # pass
            data = jwt.decode(token, os.environ['SECRET_KEY'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except Exception as error:
            return jsonify({'message': f'token: is invalid'})
                            #'error': str(error)})

        return f(*args, **kwargs)
    return decorator
