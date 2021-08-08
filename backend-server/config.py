import json

expiry = 10
PORT_START = 7000
APP_PORT = 3000
challenges = json.load(open("challenges.json"))
SECRET = "s$cr$t"
DATABASE = 'deployments.db'