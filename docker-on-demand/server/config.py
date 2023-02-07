import yaml

config = {}

with open("./config/config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

PORT_RANGE = (config["app_conf"]["port_start"], config["app_conf"]["port_end"])
APP_PORT = config["app_conf"]["app_port"]
HOST_IP = config["app_conf"]["host"]
DEBUG = config["app_conf"]["debug"]

credentials = {
    "admin": config["credentials"]["admin"],
    "user": config["credentials"]["user"]
}

images = config["images"]
