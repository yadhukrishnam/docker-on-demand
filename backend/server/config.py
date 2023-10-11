import os
import yaml
import uuid
import sys

config = {}
images = []

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
    images.append({
        "image_name": image_name,
        "local_port": config["image_data"][image_name]["local_port"],
        "env_vars": config["image_data"][image_name]["env_vars"],
        "timeout": config["image_data"][image_name]["timeout"],
    })
print ("Loaded images: ", images)

# Set credentials
credentials = {
    "admin": config["credentials"]["admin"]["password"],
    "user": config["credentials"]["user"]["password"]
}

print ("Use these credentials to login: ")
print (credentials)

SECRET_KEY = config["app_conf"]["SECRET_KEY"]
DATA_FOLDER = os.getenv('DATA_FOLDER', os.path.abspath(os.path.dirname(__file__)))
PORT_RANGE = [config["app_conf"]["port_range"]["start"], config["app_conf"]["port_range"]["end"]]
HOST_IP = config["app_conf"]["host"]

# Set default config values
# config.setdefault('enabled_images', [])
# config.setdefault('images', {})
# config.setdefault('app_conf', {})

"""

config['app_conf'].setdefault('port_start', 40000)
config['app_conf'].setdefault('port_end', 60000)
config['app_conf'].setdefault('app_port', 5015)
config['app_conf'].setdefault('host', "http://127.0.0.1")
config['app_conf'].setdefault('debug', False)
config.setdefault('credentials', {})

config['credentials'].setdefault('admin', uuid.uuid4())
config['credentials'].setdefault('user', uuid.uuid4())

print ("Use these credentials to login: ", config['credentials'])

# Set config values from environment variables
config['app_conf']['port_start'] = int(
    os.getenv('APP_PORT_START', config['app_conf']['port_start']))
config['app_conf']['port_end'] = int(
    os.getenv('APP_PORT_END', config['app_conf']['port_end']))
config['app_conf']['app_port'] = int(
    os.getenv('APP_PORT', config['app_conf']['app_port']))
config['app_conf']['host'] = os.getenv('APP_HOST', config['app_conf']['host'])
config['app_conf']['debug'] = (
    str(os.getenv('APP_DEBUG', config['app_conf']['debug'])) == 'True')



SECRET_KEY = os.getenv("SECRET_KEY", uuid.uuid4())
print (SECRET_KEY)

# Check if user was given through environment
tmp = os.getenv('APP_ADMIN_PASSWORD', None)
if tmp:
    config['credentials']['admin'] = tmp
tmp = os.getenv('APP_USER_PASSWORD', None)
if tmp:
    config['credentials']['user'] = tmp
tmp = None

PORT_RANGE = (config["app_conf"]["port_start"], config["app_conf"]["port_end"])
APP_PORT = config["app_conf"]["app_port"]
DEBUG = config["app_conf"]["debug"]



print(images)

"""