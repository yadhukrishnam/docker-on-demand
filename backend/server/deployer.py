import docker
from config import IMAGES
import re
from threading import Thread
import time


# deploy container and return container id and timeout value for clearing data from db after timeout seconds
def deploy(image_id, public_port, container_name, env_data):
    for image in IMAGES:
        if (image_id == image["image_name"]):
            print(image, flush=True)
            try:
                print("Deploying: ", image["image_name"], flush=True)
                local_port = image["local_port"]
                client = docker.from_env()
                container_name = re.sub('[^A-Za-z0-9]+', '_',
                                        container_name) + "_" + str(public_port)
                container = client.containers.run(
                    image_id, ports={f"{local_port}": public_port}, detach=True, name=container_name, environment=env_data)
                container_id = container.id
                stop_container_thread = Thread(
                    target=kill, args=(container_id, image["timeout"]))
                stop_container_thread.start()
                client.close()
                return container_id, image["timeout"]
            except Exception as e:
                print("Error:", e)
                return None, None
    return False, False


def kill(container_id, timeout):  # function to kill container after timeout seconds
    try:
        print("calling kill", flush=True)
        time.sleep(timeout)
        client = docker.from_env()
        container = client.containers.get(container_id)
        with open(f"logs/container_log_{container_id[0:10]}.txt", "w") as f:
            f.write(container.logs().decode())
        container.kill()
        container.remove()
        client.close()
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        return True


def instant_kill(container_id):  # function to kill container immediately
    try:
        print("calling instant_kill", flush=True)
        client = docker.from_env()
        container = client.containers.get(container_id)
        with open(f"logs/container_log_{container_id[0:10]}.txt", "w") as f:
            f.write(container.logs().decode())
        container.kill()
        container.remove()
        client.close()
        return True
    except:
        return False
