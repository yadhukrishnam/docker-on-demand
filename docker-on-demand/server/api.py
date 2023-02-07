from flask import Blueprint, jsonify, request,Flask
from config import *
from database import db
from sqlalchemy import text
import yaml
import docker
from threading import Thread
from deployer import deploy, instant_kill
from functools import wraps
from auth import auth
from database import Deployment
import time
import random

api = Blueprint('api', __name__)

config = ""
with open("./config/config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
        # print(images,flush=True)
    except yaml.YAMLError as exc:
        print(exc)
            
def secure(params=None):
    def decorator(f):
        @wraps(f)
        def check_authorization(*args, **kwargs):
            try:
                body = request.get_json()

                if params != None:
                    missing = [r for r in params if r not in body]
                    if missing:
                        raise ValueError("Required params not supplied.")
            except:
                response = {'status': 'fail', 'message': 'Invalid JSON body.'}
                return jsonify(response), 400

            print("Params:",params)
            print("Body",body)

            if params is None:
                return f()
            else:
                return f(* tuple(body[item] for item in params))
        return check_authorization
    return decorator

def clear_data(container_id,timeout):
    time.sleep(timeout)
    print("Trying to remove container record",flush=True)
    try:
        Deployment.query.filter_by(deployment_id=container_id).delete()
        db.session.commit()
    except Exception as e:
        print(e,flush=True)


@api.route('/api/get_images', methods=['GET'])
@auth.login_required
def get_images():
    result = []
    images = config["images"]
    for image in images:
        # print(image,flush=True)
        result.append(
            {"imagename": image["image_name"], "port": image["local_port"]})

    return jsonify({'status': 'success', "images": result})


@api.route('/api/get_deployments', methods=['POST'])
@auth.login_required
def get_deployments():
    if auth.current_user() != "admin":
        return jsonify({"status": "faill", "message": "Unauthorized"})
  
    result = {}
    client = docker.from_env()
    containers = client.containers.list()
    if(len(containers)==0):
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    for con in containers:
        result[con.attrs['Id']] = {
            "port": [con.ports[i][0]['HostPort'] if con.ports[i] else "not-found" for i in con.ports][0],
            "image_id": con.image.tags[0],
            "user_id": "admin",
            "deployment_id": con.attrs['Id'],
            "created_at": con.attrs['Created']
        }
        print(result)
    return jsonify({'status': 'success', 'deployments': result})


@api.route('/api/get_user_deployments', methods=['POST'])
@secure(["user_id"])
def get_active_deployments(user_id):
    deployments = Deployment.query.filter_by(user_id=user_id).all()
    if deployments is None:
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    else:
        result = {}
        for deployment in deployments:
            result[deployment.image_id] = {
                "url": f"{HOST_IP}:{deployment.port}/"
            }
        return jsonify({'status': 'success', 'deployments': result})


@api.route('/api/deploy', methods=['POST'])
@secure(["image_id", "user_id"])
def deploy_image(image_id, user_id):
    # deployment = Deployment.query.filter_by(
    #     user_id=user_id, image_id=image_id).first()
    # print(deployment,flush=True)
    # if deployment is None:
    while True:
        port = random.randint(PORT_RANGE[0], PORT_RANGE[1])
        port_exists = Deployment.query.filter_by(port=port).first()
        if port_exists is None:
            break

    id,timeout = deploy(image_id, port, user_id)
    deployment = Deployment(id, user_id, image_id, port, time.time())
    db.session.add(deployment)
    db.session.commit()
    clear_container_thread = Thread(target=clear_data, args=(id,timeout))
    clear_container_thread.start()
    return jsonify({"status": "success", "port": port,"timeout": timeout})
    # else:
    #     return jsonify({"status": "success", "port": deployment.port})


@api.route('/api/kill', methods=['POST'])
@secure(["deployment_id", "user_id"])
def kill_image(deployment_id, user_id):
    deployment = Deployment.query.filter_by(
        user_id=user_id, deployment_id=deployment_id).first()
    if deployment is not None:
        try:
            Deployment.query.filter_by(deployment_id=deployment.deployment_id).delete()
            db.session.commit()
        except Exception as e:
            print(e,flush=True)
        instant_kill(deployment.deployment_id)
        return jsonify({"status": "success"})
    else:
        return jsonify({'status': 'fail', 'message': 'No such deployment.'}), 404
