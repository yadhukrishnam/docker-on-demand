from flask import Blueprint, abort

import requests
from CTFd.utils.decorators import authed_only
from CTFd.utils.decorators.visibility import (
    check_account_visibility,
    check_score_visibility,
)
from CTFd.utils.config import is_teams_mode
from flask import session
from CTFd.utils.helpers import get_errors, get_infos
from CTFd.utils.user import get_ip, is_admin, authed, get_current_user, get_current_team

deployer = Blueprint("deployer", __name__)

SECRET = ""
registrar_host = "http://0.0.0.0"
registrar_port = '8000'

def user_can_get_instance():
    if is_admin():
        return True
    if not authed():
        return False
    return True

def call_registrar(body, endpoint, method='POST'):
    url = f'{registrar_host}:{registrar_port}{endpoint}'
    headers = {
        'X-Api-Token': f'{SECRET}'
    }
    
    if method == 'POST':
        return requests.post(url, json=body, headers=headers)
    elif method == 'DELETE':
        return requests.delete(url, json=body, headers=headers)
    elif method == 'GET':
        return requests.get(url, json=body, headers=headers)
    else:
        abort(404)

## Status check
@deployer.route('/get_deployment/<challenge_name>', methods=['GET'])
def get_deployments(challenge_name):
    if not user_can_get_instance():
        abort(403)
    
    clientname = get_current_user().name if not is_teams_mode() else get_current_team().name
    challenge_name = challenge_name.replace(" ","_").lower()
    body = {
        "name": clientname,
        "image": challenge_name
    }
    result = call_registrar(body, '/api/user/get_active_deployments')
    return result.json()

@deployer.route('/deploy/<challenge_name>', methods=['GET'])
def deploy_challenge(challenge_name):
    print("Deploying")
    if not user_can_get_instance():
        abort(403)
    
    clientname = get_current_user().name if not is_teams_mode() else get_current_team().name
    challenge_name = challenge_name.replace(" ","_").lower()
    if session.get('deployer_user_created') == None:
        body = {
            "name": clientname
        }
        response = call_registrar(body, '/api/user/get_or_create')
        if response.status_code == 200:
            session['deployer_user_created'] = True

    body = {
        "image": challenge_name,
        "allocated_to": clientname
    }
    result = call_registrar(body, '/api/container/deploy').json()
    return result

@deployer.route('/kill/<challenge_name>', methods=['GET'])
def kill_challenge(challenge_name):
    if not user_can_get_instance():
        abort(403)
    
    clientname = get_current_user().name if not is_teams_mode() else get_current_team().name
    challenge_name = challenge_name.replace(" ","_").lower()
    body = {
        "user": clientname,
        "image": challenge_name
    }
    result = call_registrar(body, '/api/user/container/kill')
    return result.json()
