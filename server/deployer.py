import requests
import docker
import json
import subprocess
from config import *
import re

def deploy(image_id, public_port, container_name):
    if image_id in images:
        print ("Deploying,", images[image_id])
        local_port = images[image_id]["local_port"]
        client = docker.from_env()
        container_name = re.sub('[^A-Za-z0-9]+', '_', container_name) + "_" + str(public_port)
        container = client.containers.run(image_id, ports={f"{local_port}" : public_port}, detach=True, name=container_name)
        container_id = container.id
        client.close()
        return container_id
    return None

def kill(container_id):
    try:
        client = docker.from_env()
        container = client.containers.get(container_id)
        container.kill()
        container.remove()
        client.close()
    except:
        return False
    finally:
        return True