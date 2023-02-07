from flask import Flask, request, jsonify, redirect, session, url_for
from flask.templating import render_template
import logging
import requests
import yaml
import hashlib
import json
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'h4ck3r43v3r9875SDF'
basedir = os.path.abspath(os.path.dirname(__file__))

# logging.basicConfig(filename='debug.log', level=logging.WARNING,
                    # format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


CONFIG_PATH = "./config.yaml"
config = ""
with open(CONFIG_PATH, "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


CHALL_NAMES = config["images"]
API_URL = "http://localhost:5000"
print(CHALL_NAMES)

def PoW():
    x = os.urandom(16)
    target = hashlib.md5(x).hexdigest()
    out = f"MD5(X = {x[:13].hex()}+{'?'*6}) = " + target
    return x,target,out

# def solvepow(x, target):
#     x = bytes.fromhex(x)
#     target = bytes.fromhex(target)
#     for i in range(256**3):
#         if hashlib.md5(x + i.to_bytes(3, "big")).digest() == target:
#             return x.hex()+hex(i)[2:]

@app.route("/challenge/<id>")
def index(id):
    try:
        x,target,out = PoW()
        session["target"] = target
        session["x"] = x[:13].hex()
        return render_template("index.html",chall_name=CHALL_NAMES[int(id)-1]["image_name"],question=out)
    except:
        return {"error":"invalid id specified"}
    

@app.route("/deploy/challenge/<id>",methods=["POST"])
def deploy(id):
    try:
        print(request)
        if(request.form['answer'] == None):
            raise  
        answer = request.form['answer']
        print(answer,session['target'],flush=True)
        if(hashlib.md5(bytes.fromhex(session['x']+answer)).hexdigest() == session["target"]): 
            # int(session["num1"])*int(session["num2"])
            r = requests.post(API_URL+"/api/deploy",json={"image_id":CHALL_NAMES[int(id)-1]["image_name"],"user_id":"admin"})
            print(r.text)
            print(json.loads(r.text)['port'],flush=True)
            session['target'] = "chavar"
            return {"id":id,"port":json.loads(r.text)['port'],"timeout":json.loads(r.text)['timeout'],"status":"SUCCESS"},200
        return {"id":id,"status":"FAIL"},400
    except Exception as e:
        print("Error:",str(e))
        return {"id":id,"status":"error"},400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=False)
