from flask_httpauth import HTTPBasicAuth
import jwt
from functools import wraps
from config import SECRET_KEY, credentials
from flask import request, jsonify

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in credentials and \
            (credentials.get(username) == password):
        return username


def secure(params=None):
    def decorator(f):
        @wraps(f)
        def check_authorization(*args, **kwargs):
            try:
                bearer = request.headers.get("Authorization")
                if bearer:
                    import base64
                    bearer = bearer.split(" ")[1]
                    credential = base64.b64decode(bearer)
                    body = request.get_json()
                    assert credential == f"admin:{credentials['admin']}".encode()
                else:
                    body = request.get_json()["body"]
                    body = jwt.decode(body, SECRET_KEY, algorithms=["HS256"])
                    if params != None:
                        missing = [r for r in params if r not in body]
                        if missing:
                            raise ValueError("Required params not supplied.")
            except Exception as e:
                response = {'status': 'fail',
                            'message': f'Invalid JSON body {e}'}
                return jsonify(response), 400

            if params is None:
                return f()
            else:
                return f(* tuple(body[item] for item in params))
        return check_authorization
    return decorator
