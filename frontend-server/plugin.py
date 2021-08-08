from flask import Flask, request
import requests
import jwt

app = Flask(__name__)

SECRET = "s$cr$t"
challenge_server = "http://192.168.0.106:3000" 

@app.route("/get_deployments", methods=["POST"])
def get_deployments():
    body = request.get_json()
    data = {
        "user_id": body["user_id"]
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(challenge_server + "/get_deployments", json={"body": encoded}).json()
    return r

@app.route('/request_deploy/<challenge_id>', methods=['POST'])
def deploy_challenge(challenge_id):
    body = request.get_json()
    data = {
        "challenge_id": challenge_id,
        "user_id": body["user_id"]
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(challenge_server + "/deploy", json={"body": encoded}).json()
    return r

@app.route('/request_kill', methods=['POST'])
def kill_challenge():
    body = request.get_json()
    data = {
        "challenge_id": body["challenge_id"],
        "user_id": body["user_id"],
        "deployment_id": body["deployment_id"]
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(challenge_server + "/kill", json={"body": encoded}).json()
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
