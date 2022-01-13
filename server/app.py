from flask import Flask, request, jsonify, redirect
from flask.templating import render_template
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from sqlalchemy import text
from database import db, Deployment
from config import credentials, images, PORT_RANGE
import threading
import os
import logging
import random
import time
from deployer import *

app = Flask(__name__)
auth = HTTPBasicAuth()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

logging.basicConfig(filename='debug.log', level=logging.WARNING, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def secure(params=None):
    def decorator(f):
        @wraps(f)
        def check_authorization(*args, **kwargs):
            try:
                body = request.get_json()

                if params != None:
                    missing = [r for r in params if r not in body]
                    if missing:
                        raise ValueError("Required params not supplied.")
            except:
                response = {'status': 'fail', 'message': 'Invalid JSON body.'}
                return jsonify(response), 400

            if params is None:
                return f()
            else:
                return f(* tuple(body[item] for item in params))
        return check_authorization
    return decorator


def auto_clear():
    sql = text(
        'Select * FROM deployment WHERE :time - created_at > 60').bindparams(time=time.time())
    expired_deployments = db.session.execute(sql).all()
    for deployment in expired_deployments:
        remove_deployment(deployment[0])
    db.session.commit()
    threading.Timer(20, auto_clear).start()


def remove_deployment(deployment_id):
    kill(deployment_id)
    Deployment.query.filter_by(deployment_id=deployment_id).delete()
    db.session.commit()


@app.errorhandler(Exception)
def server_error(err):
    app.logger.exception(err)
    return jsonify({'status': 'fail'})


@auth.verify_password
def verify_password(username, password):
    if username in credentials and \
            (credentials.get(username) == password):
        return username


@app.route('/api/get_images', methods=['GET'])
@auth.login_required
def get_images():
    result = []
    for image in images:
        result.append(
            {"imagename": image, "port": images[image]["local_port"]})

    return jsonify({'status': 'success', "images": result})


@app.route('/api/get_deployments', methods=['POST'])
@auth.login_required
def get_deployments():
    if auth.current_user() != "admin":
        return jsonify({"status": "fail", "message": "Unauthorized"})

    deployments = Deployment.query.filter_by().all()

    if deployments is None:
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    else:
        result = {}
        for deployment in deployments:
            print(deployment.user_id)
            result[deployment.image_id] = {
                "port": deployment.port,
                "user_id": deployment.user_id,
                "deployment_id": deployment.deployment_id,
                "created_at": deployment.created_at
            }
        return jsonify({'status': 'success', 'deployments': result})


@app.route('/api/get_user_deployments', methods=['POST'])
@auth.login_required
@secure(["user_id"])
def get_active_deployments(user_id):
    deployments = Deployment.query.filter_by(user_id=user_id).all()
    if deployments is None:
        return jsonify({'status': 'fail', 'message': 'No deployments found.'}), 404
    else:
        result = {}
        for deployment in deployments:
            result[deployment.image_id] = {
                "url": f"{HOST_IP}:{deployment.port}/"
            }
        return jsonify({'status': 'success', 'deployments': result})


@app.route('/api/deploy', methods=['POST'])
@auth.login_required
@secure(["image_id", "user_id"])
def deploy_image(image_id, user_id):
    deployment = Deployment.query.filter_by(
        user_id=user_id, image_id=image_id).first()
    if deployment is None:
        while True:
            port = random.randint(PORT_RANGE[0], PORT_RANGE[1])
            port_exists = Deployment.query.filter_by(port=port).first()
            if port_exists is None:
                break

        id = deploy(image_id, port, user_id)
        deployment = Deployment(id, user_id, image_id, port, time.time())
        db.session.add(deployment)
        db.session.commit()
        return jsonify({"status": "success", "port": port})
    else:
        print(deployment)
        return jsonify({"status": "success", "port": deployment.port})


@app.route('/api/kill', methods=['POST'])
@auth.login_required
@secure(["image_id", "user_id"])
def kill_image(image_id, user_id):
    deployment = Deployment.query.filter_by(
        user_id=user_id, image_id=image_id).first()
    if deployment is not None:
        remove_deployment(deployment.deployment_id)
        return jsonify({"status": "success"})
    else:
        return jsonify({'status': 'fail', 'message': 'No such deployment.'}), 404


@app.route("/")
@auth.login_required
def index():
    return redirect("/dashboard")


@app.route("/dashboard")
@auth.login_required
def dashboard():
    return render_template("index.html")


@app.route("/deployments")
@auth.login_required
def deployments():
    return render_template("deployments.html")


@app.route("/logout")
@auth.login_required
def logout():
    return "Bye!", 401


with app.app_context():
    db.create_all()
    auto_clear()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=APP_PORT, debug=True)
