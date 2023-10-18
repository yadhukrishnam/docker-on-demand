from flask import Blueprint, jsonify
from config import IMAGES, HOST_IP, PORT_RANGE
from deployer import deploy
from functools import wraps
from auth import auth
from database import db, Deployment
from database import Deployment
import time
import random
import docker
from deployer import deploy, instant_kill
from threading import Thread
from auth import secure

api = Blueprint('api', __name__)




def get_image_info(image_name):
    global IMAGES
    print ("Images available",  IMAGES)
    for image in IMAGES:
        if image['image_name'] == image_name:
            return image


def clear_data(container_id, timeout):  # function to clear data after timeout
    time.sleep(timeout)
    print("Trying to remove container record", flush=True)
    try:
        # can remove this after docker api is independent of db
        Deployment.query.filter_by(deployment_id=container_id).delete()
        db.session.commit()
    except Exception as e:
        print(e, flush=True)


@api.route('/api/get_images', methods=['GET'])
@auth.login_required
def get_images():
    result = []
    for image in IMAGES:
        result.append(
            {"imagename": image["image_name"], "port": image["local_port"]})
    return jsonify({'status': 'success', "images": result})


@api.route('/api/get_deployments', methods=['POST'])  # get all deployments
@auth.login_required
def get_deployments():
    result = {}
    client = docker.from_env()
    containers = client.containers.list()
    if (len(containers) == 0):
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    for con in containers:
        result[con.attrs['Id'][:10]] = {
            "port": [con.ports[i][0]['HostPort'] if con.ports[i] else "not-found" for i in con.ports][0],
            "image_id": con.image.tags[0],
            "user_id": con.attrs['Name'].split("_")[0],
            "deployment_id": con.attrs['Id'][:10],
            "created_at": con.attrs['Created']
        }
        print(result)
    return jsonify({'status': 'success', 'deployments': result})


@api.route('/api/get_user_deployments', methods=['POST'])
@secure(["user_id", "challenge_name"])
def get_active_deployments(user_id, image_id):
    deployments = Deployment.query.filter_by(user_id=user_id, image_id=image_id).first()
    if deployments is None:
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    else:
        return jsonify({'status': 'success', 'host': HOST_IP, "port": deployments.port})


# deploy image on random port in range PORT_RANGE in config file
@api.route('/api/deploy', methods=['POST'])
@secure(["image_id", "user_id"])
def deploy_image(image_id, user_id):
    deployment = Deployment.query.filter_by(user_id=user_id, image_id=image_id).first()
    if deployment is None:
        while True:
            port = random.randint(PORT_RANGE[0], PORT_RANGE[1])
            port_exists = Deployment.query.filter_by(
                port=port).first()  # Replace with docker api
            if port_exists is None:
                break

        image_info = get_image_info(image_id)
        id, timeout = deploy(image_id, port, user_id,
                            image_info["env_vars"])  # deploy image
        print (id, image_info)
        deployment = Deployment(id, user_id, image_id, port, time.time())
        db.session.add(deployment)
        db.session.commit()
        clear_container_thread = Thread(target=clear_data, args=(
            id, timeout))  # start thread to clear data after timeout
        clear_container_thread.start()  # start thread
        return jsonify({"status": "success", "host": HOST_IP, "port":port, "timeout": timeout})
    else:
        print ("Deployment already exists. Returning data.")
        return jsonify({"status": "success", "host": HOST_IP, "port": deployment.port})


# kill image by deployment id (docker container id)
@api.route('/api/kill', methods=['POST'])
@secure(["image_id", "user_id"])
def kill_image(image_id, user_id):
    if user_id != "admin":
        deployment = Deployment.query.filter_by(user_id=user_id, image_id=image_id).first()
    else:
        deployment = Deployment.query.filter_by(image_id=image_id).first()
    db.session.delete(deployment)
    db.session.commit()
    if deployment is None:
        return jsonify({'status': 'fail', 'message': 'No such deployment.'}), 404
    else:
        deployment_id = deployment.deployment_id
        if instant_kill(deployment_id) == True:
            return jsonify({"status": "success", "deployment_id": deployment_id})
        else:
            return jsonify({'status': 'fail', 'message': 'Error killing deployment.'}), 404
    return jsonify({'status': 'fail', 'message': 'Something went wrong.'}), 404