from flask import Flask, request, jsonify, g
import requests
import jwt
import uuid
import sqlite3
import subprocess
import docker
import json
import sys
import threading
from deployer import *

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def auto_clear():
    conn = sqlite3.connect(DATABASE)
    cur = conn.execute("SELECT deployment_id FROM  deployments WHERE ROUND((JULIANDAY(current_timestamp) - JULIANDAY(created_at)) * 1440) > ?", (expiry, ))
    expired_deployments = cur.fetchall()
    conn.close()
    for deployment in expired_deployments:
        remove_deployment(deployment[0])

    threading.Timer(60, auto_clear).start()

def remove_deployment(deployment_id):
    kill(deployment_id)
    conn = sqlite3.connect(DATABASE)
    cur = conn.execute("DELETE FROM deployments WHERE deployment_id = ?", (deployment_id, ))
    conn.commit()
    conn.close()

@app.route('/get_deployments', methods=['POST'])
def get_deployments():
    body = request.get_json()["body"]
    try:
        payload = jwt.decode(body, SECRET, algorithms=["HS256"])
        user_id = str(payload["user_id"])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return jsonify({'status': 'fail', 'message': 'Token is invalid'})  

    deployments = query_db("SELECT challenge_id, deployment_id FROM deployments WHERE user_id = ?", (user_id, )) 
    if deployments is None or len(deployments) == 0:
        return jsonify({'status': 'fail', 'message': 'No deployments found.'})  
    else:
        result = {}
        for row in deployments:
            result[row[0]] = {
                "deployment_id": row[1],
            }
        return jsonify({'status': 'success', 'deployments': result})  
    

@app.route('/deploy', methods=['POST'])
def deploy_challenge():
    body = request.get_json()["body"]
    try:
        payload = jwt.decode(body, SECRET, algorithms=["HS256"])
        challenge_id = str(payload["challenge_id"])
        user_id = str(payload["user_id"])

    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return jsonify({'status': 'fail', 'message': 'Token is invalid'})
        
    deployment = query_db("SELECT * FROM deployments WHERE user_id = ? AND challenge_id = ?", (user_id, challenge_id) , True)

    if deployment is None:
        id, port = deploy(challenge_id)
        conn = sqlite3.connect(DATABASE)
        conn.execute("INSERT INTO deployments  VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)", (id, user_id, challenge_id, str(port)))
        conn.commit()
        conn.close()

        return jsonify({"status":"success", 'deployment_id': id, "port": port})
    else:
        print(deployment)
        return jsonify({"status":"success", 'deployment_id': deployment[0], "port" : deployment[3]})

    
@app.route('/kill', methods=['POST'])
def kill_challenge():
    body = request.get_json()["body"]
    try:
        payload = jwt.decode(body, SECRET, algorithms=["HS256"])
        challenge_id = str(payload["challenge_id"])
        user_id = str(payload["user_id"])
        deployment_id = str(payload["deployment_id"])

    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return jsonify({'status': 'fail', 'message': 'Token is invalid'})
    
    deployment = query_db("SELECT * FROM deployments WHERE user_id = ? AND challenge_id = ? AND deployment_id = ?", (user_id, challenge_id, deployment_id) , True)
    
    if deployment is not None:
        port = deployment[3]
        print ("Deleting deployment at", port)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM deployments WHERE user_id = ? AND challenge_id = ? ", (user_id, challenge_id,))
        kill(deployment_id)
        conn.commit()
        conn.close()
        return jsonify({"status":"success"})
    else:
        return jsonify({'status':'fail', 'message': 'No such deployment.'})
        


if __name__ == '__main__':
    print(sys.argv[1:])
    if "--build" in sys.argv[1:]:
        print ("Starting build..")
        for challenge in challenges:
            build_image(challenges[challenge])
    
    if "--autokill" in sys.argv[1:]:
        print ("Started with auto kill")
        auto_clear()

    conn = sqlite3.connect(DATABASE)
    conn.execute('''CREATE TABLE IF NOT EXISTS deployments (deployment_id, user_id, challenge_id, port, created_at); ''')
    conn.close()
    app.run(host='0.0.0.0', port=9999, debug=True)