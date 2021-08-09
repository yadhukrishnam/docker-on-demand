from flask import Flask, request, jsonify
from functools import wraps
import requests
import jwt
import sys
import threading
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from sqlalchemy import text
from datetime import datetime
from deployer import *

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Deployment(db.Model):
    deployment_id = db.Column(  db.String(65), primary_key=True)
    user_id = db.Column(db.String(200), nullable=False)
    challenge_id = db.Column(db.String(200), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    def __init__(self, deployment_id, user_id, challenge_id, port):
        self.deployment_id = deployment_id
        self.user_id = user_id
        self.challenge_id = challenge_id
        self.port = port

def jwt_verification(params):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try: 
                body = request.get_json()["body"]
                payload = jwt.decode(body, SECRET, algorithms=["HS256"])
                missing = [r for r in params if r not in payload]
                if missing:
                    raise ValueError("Required params not supplied.")
            except:
                response = {'status': 'fail', 'message': 'Invalid token supplied.'}
                return jsonify(response), 400
            return fn(* tuple(payload[item] for item in params))
        return wrapper
    return decorator

def auto_clear():
    current_timestamp = datetime.utcnow()
    sql = text('SELECT deployment_id FROM Deployment WHERE ROUND((JULIANDAY(created_at) - JULIANDAY(current_timestamp)) * 1440) > :expiry').bindparams(expiry=expiry)
    expired_deployments = db.session.execute(sql).all()
    for deployment in expired_deployments:
        remove_deployment(deployment[0])
    db.session.commit()
    threading.Timer(60, auto_clear).start()

def remove_deployment(deployment_id):
    kill(deployment_id)
    Deployment.query.filter_by(deployment_id=deployment_id).delete()
    db.session.commit()

@app.route('/get_deployments', methods=['POST'])
@jwt_verification(["user_id"])
def get_deployments(user_id):
    deployments = Deployment.query.filter_by(user_id=user_id).all()
    if deployments is None or len(deployments) == 0:
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    else:
        result = {}
        for deployment in deployments:
            result[deployment.challenge_id] = {
                "url": f"{HOST_IP}:{deployment.port}/"
            }
        return jsonify({'status': 'success', 'deployments': result})  
    
@app.route('/deploy', methods=['POST'])
@jwt_verification(["challenge_id", "user_id"])
def deploy_challenge(challenge_id, user_id):   
    deployment = Deployment.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if deployment is None:
        id, port = deploy(challenge_id)
        deployment = Deployment(id, user_id, challenge_id, port)
        db.session.add(deployment)
        db.session.commit()
        return jsonify({"status":"success", "url": f"{HOST_IP}:{port}/"})
    else:
        print(deployment)
        return jsonify({"status":"success", "url" : f"{HOST_IP}:{deployment[3]}/"})

    
@app.route('/kill', methods=['POST'])
@jwt_verification(["challenge_id", "user_id"])
def kill_challenge(challenge_id, user_id):
    deployment = Deployment.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if deployment is not None:
        remove_deployment(deployment.deployment_id)
        return jsonify({"status":"success"})
    else:
        return jsonify({'status':'fail', 'message': 'No such deployment.'}), 404
        
if __name__ == '__main__':
    if "--build" in sys.argv[1:]:
        print ("Starting build..")
        for challenge in challenges:
            build_image(challenges[challenge])
    
    if "--autokill" in sys.argv[1:]:
        print ("Started with auto kill..")
        auto_clear()

    db.create_all()
    app.run(host='0.0.0.0', port=APP_PORT, debug=False) 