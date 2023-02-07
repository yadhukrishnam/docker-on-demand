import os
import yaml

config = {}

with open("./config/config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# Set default config values
config.setdefault('images', {})
config.setdefault('app_conf', {})
config['app_conf'].setdefault('port_start', 40000)
config['app_conf'].setdefault('port_end', 60000)
config['app_conf'].setdefault('app_port', 5015)
config['app_conf'].setdefault('host', "http://127.0.0.1")
config['app_conf'].setdefault('debug', False)
config.setdefault('credentials', {})
#config['credentials'].setdefault('admin', 'admin')
#config['credentials'].setdefault('user', 'user')

# Set config values from environment variables
config['app_conf']['port_start'] = int(os.getenv('APP_PORT_START', config['app_conf']['port_start']))
config['app_conf']['port_end'] = int(os.getenv('APP_PORT_END', config['app_conf']['port_end']))
config['app_conf']['app_port'] = int(os.getenv('APP_PORT', config['app_conf']['app_port']))
config['app_conf']['host'] = os.getenv('APP_HOST', config['app_conf']['host'])
config['app_conf']['debug'] = (str(os.getenv('APP_DEBUG', config['app_conf']['debug'])) == 'True')
DATA_FOLDER = os.getenv('DATA_FOLDER', os.path.abspath(os.path.dirname(__file__)))

# Get images from env variables
tmp = os.getenv('APP_IMAGES', None)
if tmp:
    config['images'] = {}
    tmp = tmp.split(',')
    for image in tmp:
        image = image.split('|')
        config['images'][image[0]] = {
            'local_port' : int(image[1])
        }


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
HOST_IP = config["app_conf"]["host"]
DEBUG = config["app_conf"]["debug"]

credentials = {
    "admin": config["credentials"]["admin"],
    "user": config["credentials"]["user"]
}

images = config["images"]
