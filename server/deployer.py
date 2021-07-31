from flask import Flask, request, jsonify, g
import requests
import subprocess
import docker
import json

app = Flask(__name__)

def build_images(challenges):
    client = docker.from_env()
    for challenge in challenges:
        subprocess.run(["docker-compose build"], cwd=challenges[challenge]["path"], shell=True, check=True)
    client.close()

def deploy(image, local_port, public_port):
    client = docker.from_env()
    container = client.containers.run(image, ports={f"{public_port}" : local_port}, detach=True)
    container_id = container.id
    client.close()
    return container_id

def kill_container(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.kill()
    client.close()

@app.route("/request_deploy", methods=["POST"])
def request_deploy():
    body = request.get_json()
    image = body["image"]
    local_port = body["local_port"]
    public_port = body["public_port"]
    container_id  = deploy(image, local_port, public_port)
    return jsonify({"status": "success", "container_id" : container_id})

@app.route("/request_kill", methods=["POST"])
def request_kill():
    body = request.get_json()
    container_id = body["container_id"]
    kill_container(container_id)
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)