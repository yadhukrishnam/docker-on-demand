from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy_utils import StringEncryptedType
from flask_login import UserMixin, login_user,LoginManager, login_required, logout_user, current_user 

_key = "l33tEncryptionzz"
db = SQLAlchemy()
app = Flask(__name__)

class Deployment(db.Model):
    __tablename__ = "deployment"
    deployment_id = db.Column(db.String(65), primary_key=True)
    user_id = db.Column(db.String(200), nullable=False)
    image_id = db.Column(db.String(200), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(80), nullable=False)


    def __init__(self, deployment_id, user_id, image_id, port, created_at):
        self.deployment_id = deployment_id
        self.user_id = user_id
        self.image_id = image_id
        self.port = port
        self.created_at = created_at
        
class Users(db.Model, UserMixin): #Parent table to solvedchalls.
    __tablename__ = "users"
    id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.String(200), primary_key=True)
    username = db.Column(StringEncryptedType(db.String, _key), unique=True, nullable=False)
    password = db.Column(StringEncryptedType(db.String, _key), nullable=False)
    email = db.Column(db.String)
    total_points = db.Column(db.Integer, default=0) # Added total_points column
    solvedChalls = db.relationship('SolvedChallenges', backref='users')

    def update_total_points(self):
        solved_challenges = SolvedChallenges.query.filter_by(user_id=self.user_id).all()
        total_points = 0
        for solved_challenge in solved_challenges:
            total_points += solved_challenge.point
        self.total_points = total_points
        db.session.commit()
        
    def __init__(self, id, user_id, username, password, email, total_points):
            self.id = id
            self.user_id = user_id
            self.username = username
            self.password = password
            self.email = email
            self.total_points=total_points

class Challenges(db.Model):
    __tablename__ = "challenges"
    chall_id = db.Column(db.Integer, primary_key=True)
    chall_name = db.Column(db.String(200), nullable=False)
    chall_point = db.Column(db.Integer, nullable=False)
    chall_description = db.Column(db.String(1000), nullable=False)
    solvedChalls = db.relationship('SolvedChallenges', backref='challenges')

    def __init__(self, chall_id, chall_name, chall_point, chall_description):
            self.chall_id = chall_id
            self.chall_name = chall_name
            self.chall_point = chall_point
            self.chall_description = chall_description
        
class SolvedChallenges(db.Model): #Child table to users.
    __tablename__ = "solvedchalls"
    # autoincriment id
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    chall_id = db.Column(db.Integer, db.ForeignKey('challenges.chall_id'))
    user_id = db.Column(db.String(200), db.ForeignKey('users.user_id'))
    solved_chall_name = db.Column(db.String(200), nullable=False)
    point = db.Column(db.Integer, nullable=False)

    def __init__(self, chall_id, user_id, point, solved_chall_name):
        self.chall_id = chall_id
        self.user_id = user_id
        self.solved_chall_name = solved_chall_name
        self.point = point
          
    #To create the tables in the models, open a flask shell and do 'from database import db, Users, Challenges, SolvedChallenges, Deployment' and 'db.create_all()'
    #If the dummyData.py isn't working, open the flask shell and run the commands inside the shell.
