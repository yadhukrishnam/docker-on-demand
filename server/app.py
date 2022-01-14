from flask import Flask, request, jsonify, redirect
from flask.templating import render_template
from database import db
from config import *
from auth import auth
import os
import logging
from api import api

app = Flask(__name__)
app.register_blueprint(api)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

logging.basicConfig(filename='debug.log', level=logging.WARNING,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.errorhandler(Exception)
def server_error(err):
    api.logger.exception(err)
    return jsonify({'status': 'fail'})


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=APP_PORT, debug=DEBUG)
