from flask import Flask, request, jsonify, redirect, session, url_for
from flask.templating import render_template
#from flask_wtf import RecaptchaField
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
import logging, uuid
import requests
import yaml
import hashlib
import json
import random
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = str(uuid.uuid4())
# logging.basicConfig(filename='debug.log', level=logging.WARNING,
                    # format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


CONFIG_PATH = "./config.yaml"
config = ""
with open(CONFIG_PATH, "r") as stream: # load config
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


CHALL_NAMES = config["images"]
API_URL = "http://localhost:1337"
print(CHALL_NAMES)

def PoW():
    x = os.urandom(16)
    target = hashlib.md5(x).hexdigest()
    out = f"MD5(X = {x[:13].hex()}+{'?'*6}) = " + target
    return x,target,out

# my code end
@app.route("/challenge/<id>") # get all images 
def index(id):
    try:
        x,target,out = PoW()
        session["target"] = target
        session["x"] = x[:13].hex()
        return render_template("index.html",chall_name=CHALL_NAMES[int(id)-1]["image_name"],question=out)
    except Exception as e:
        return {"error":f"invalid id specified: {e}"},400
    

@app.route("/deploy/challenge/<id>",methods=["POST"]) # get all images 
def deploy(id): 
    try:
        print(request)
        if(request.form['answer'] == None): # check if answer is present
            raise  
        answer = request.form['answer']
        print(answer,session['target'],flush=True)
        if(hashlib.md5(bytes.fromhex(session['x']+answer)).hexdigest() == session["target"]):  # check if answer is correct
            r = requests.post(API_URL+"/api/deploy",json={"image_id":CHALL_NAMES[int(id)-1]["image_name"],"user_id":"admin"}) # deploy container 
            print(r.text)
            print(json.loads(r.text)['port'],flush=True)
            session['target'] = "chavar"
            return {"id":id,"port":json.loads(r.text)['port'],"timeout":json.loads(r.text)['timeout'],"status":"SUCCESS"},200
        return {"id":id,"status":"FAIL"},400
    except Exception as e:
        print("Error:",str(e))
        return {"id":id,"status":"error"},400
    



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)