import json

PORT_START = 40000
PORT_END = 60000
APP_PORT = 5015
HOST_IP = "http://challenge.host"
SECRET = "<redacted>"
challenges = json.load(open("challenges.json"))