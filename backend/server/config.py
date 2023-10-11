import os
import yaml
import sys
import uuid

config = {}
IMAGES = []

with open("./config/config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        print ("Unable to load configuration, exiting.")
        sys.exit(0)

# Set enabled images
data = config["image_data"]

for image_name in data:
    IMAGES.append({
        "image_name": image_name,
        "local_port": config["image_data"][image_name]["local_port"],
        "env_vars": config["image_data"][image_name]["env_vars"],
        "timeout": config["image_data"][image_name]["timeout"],
    })
print ("Loaded images: ", IMAGES)

# Set credentials
credentials = {
    "admin": config["credentials"]["admin"]["password"],
    "user": config["credentials"]["user"]["password"]
}

print ("Use these credentials to login: ")
print (credentials)

SECRET_KEY = os.getenv('SECRET_KEY', uuid.uuid4())
DATA_FOLDER = os.getenv('DATA_FOLDER', os.path.abspath(os.path.dirname(__file__)))
PORT_RANGE = [config["app_conf"]["port_range"]["start"], config["app_conf"]["port_range"]["end"]]
HOST_IP = config["app_conf"]["host"]

