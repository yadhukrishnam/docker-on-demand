from flask import Flask, request
import requests
import jwt

app = Flask(__name__)

SECRET = "s$cr$t"
challenge_server = "http://192.168.0.106:9999"

@app.route('/request_deploy/<int:challenge_id>', methods=['POST'])
def deploy_challenge(challenge_id):
    body = request.get_json()
    data = {
        "challenge_id": challenge_id,
        "user_id": body["user_id"]
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(challenge_server + "/deploy", json={"body": encoded}).json()
    return r

@app.route('/request_kill/<int:challenge_id>', methods=['POST'])
def kill_challenge(challenge_id):
    body = request.get_json()
    data = {
        "challenge_id": challenge_id,
        "user_id": body["user_id"],
        "deployment_id": body["deployment_id"]
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(challenge_server + "/kill", json={"body": encoded}).json()
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)