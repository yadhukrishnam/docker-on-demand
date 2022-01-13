import json

PORT_START = 40000
PORT_END = 60000
APP_PORT = 5015
HOST_IP = "http://host"

credentials = {
    "admin": "admin",
    "user" : "user"
}

images = json.load(open("./config/images.json"))