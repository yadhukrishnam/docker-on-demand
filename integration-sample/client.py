from flask import Flask, request
import requests
from config import BACKEND_API_URL

app = Flask(__name__)

@app.route('/request_deploy', methods=['POST'])
def deploy_challenge():
    body = request.get_json()
    data = {
        "image_id": body["image_id"],
        "user_id": body["user_id"]
    }
    r = requests.post(BACKEND_API_URL + "/deploy", json=data).json()
    return r

@app.route('/request_kill', methods=['POST'])
def kill_challenge(challenge_id):
    body = request.get_json()
    data = {
        "challenge_id": body["challenge_id"],
        "user_id": body["user_id"],
        "deployment_id": body["deployment_id"]
    }
    r = requests.post(BACKEND_API_URL + "/kill", json=data).json()
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=False)