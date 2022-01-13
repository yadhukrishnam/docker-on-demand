import json

PORT_RANGE = (40000, 60000)
APP_PORT = 5015
HOST_IP = "http://host"

credentials = {
    "admin": "admin",
    "user" : "user"
}

images = json.load(open("./config/images.json"))