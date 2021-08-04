import requests
import docker
import json
from config import *

def build_images(challenges):
    client = docker.from_env()
    for challenge in challenges:
        subprocess.run(["docker-compose build"], cwd=challenges[challenge]["path"], shell=True, check=True)
    client.close()

def deploy(challenge_id):
    global PORT_START

    if challenge_id in challenges:
        print ("Deploying,", challenges[challenge_id])
        local_port = challenges[challenge_id]["local_port"]
        public_port = PORT_START
        PORT_START += 1
        client = docker.from_env()
        container = client.containers.run(challenge_id, ports={f"{local_port}" : public_port}, detach=True)
        container_id = container.id
        client.close()
        return container_id, public_port
        
    return None

def kill(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.kill()
    container.remove()
    client.close()
    return True