import requests
import docker
import json
import subprocess
from config import *

def deploy(challenge_id, public_port, container_name):
    if challenge_id in challenges:
        print ("Deploying,", challenges[challenge_id])
        local_port = challenges[challenge_id]["local_port"]
        client = docker.from_env()
        container = client.containers.run(challenge_id, ports={f"{local_port}" : public_port}, detach=True, name=container_name)
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