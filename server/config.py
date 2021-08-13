import json

expiry = 2
PORT_START = 40000
PORT_END = 60000
APP_PORT = 5015
HOST_IP = "http://web.challenge.bi0s.in"
CLIENT_IP = ""
SECRET = "dff963b83292e48320b1b97f2382cd95320f72a8525566a7d8b4b7781680093bf4bde44644f74c6110e97d2eb3a41e94b5ff2f2af14ba26b1f59336fb8ab4c0b"
challenges = json.load(open("challenges.json"))