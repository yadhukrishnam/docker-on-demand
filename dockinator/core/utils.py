import docker
import hashlib
import random
import string
from dockinator.settings import POW_STRENGTH

def get_docker_client():
    return docker.from_env()

def is_image_available(image_name, image_tag):
    locally_available_images = []
    for image in get_docker_client().images.list():
        try:
            locally_available_images.append(image.tags[0])
        except IndexError:
            continue
    return f"{image_name}:{image_tag}" in locally_available_images

def deploy_container(image, container_name, port_to_expose, allocated_port):
    client = get_docker_client()
    container = client.containers.run(
        image,
        name=container_name,
        ports={f"{port_to_expose}/tcp": allocated_port},
        detach=True)
    return container.id


def get_container_logs(container_id):
    client = get_docker_client()
    container = client.containers.get(container_id)
    return container.logs()


def kill_container(container_id):
    client = get_docker_client()
    container = client.containers.get(container_id)
    logs = get_container_logs(container_id)
    container.kill()
    return logs


def generate_pow():
    """
    Generates a random string and hashes it with md5 to generate a proof of work.
    """
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=25))
    hash = hashlib.md5(random_string.encode()).hexdigest()
    return random_string[:-1 * POW_STRENGTH], hash, POW_STRENGTH
