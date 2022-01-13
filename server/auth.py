from flask_httpauth import HTTPBasicAuth
from config import credentials


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in credentials and \
            (credentials.get(username) == password):
        return username
