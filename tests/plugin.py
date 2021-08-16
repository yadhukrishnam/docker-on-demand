from flask import Flask, request
import requests
import jwt
from config import * 

app = Flask(__name__)

@app.route("/get_deployments", methods=["POST"])
def get_deployments():
    body = request.get_json()
    data = {
        "user_id": body["user_id"]
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(image_server + "/get_deployments", json={"body": encoded}).json()
    return r

@app.route('/request_deploy/<image_id>', methods=['POST'])
def deploy_image(image_id):
    body = request.get_json()
    data = {
        "image_id": image_id,
        "user_id": body["user_id"]
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(image_server + "/deploy", json={"body": encoded}).json()
    return r

@app.route('/request_kill', methods=['POST'])
def kill_image():
    body = request.get_json()
    data = {
        "image_id": body["image_id"],
        "user_id": body["user_id"],
    }
    encoded = jwt.encode(data, SECRET, algorithm="HS256")
    r = requests.post(image_server + "/kill", json={"body": encoded}).json()
    return r


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
