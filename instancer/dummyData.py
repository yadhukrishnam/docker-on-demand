from flask import Flask
from datetime import datetime
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database import Users, Challenges, SolvedChallenges, db

# create the database engine and create all tables
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///' + \
    os.path.join(basedir, 'database.sqlite'), echo=True)
with app.app_context():
    db.create_all()

    # create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # create some test data
    user1 = Users(id=1, user_id="user1", username="john", password="password123", email="john@example.com", total_points=0)
    user2 = Users(id=2, user_id="user2", username="jane", password="password456", email="jane@example.com", total_points=0)
    user3 = Users(id=3, user_id="user3", username="jack", password="password789", email="jack@example.com", total_points=0)

    chall1 = Challenges(chall_id=1, chall_name="Challenge 1", chall_point=100, chall_description="This is the first challenge")
    chall2 = Challenges(chall_id=2, chall_name="Challenge 2", chall_point=200, chall_description="This is the second challenge")
    chall3 = Challenges(chall_id=3, chall_name="Challenge 3", chall_point=300, chall_description="This is the third challenge")

    solved_chall1 = SolvedChallenges(id=1, chall_id=1, user_id="user1", point=100, solved_chall_name=chall1.chall_name)
    solved_chall2 = SolvedChallenges(id=2, chall_id=2, user_id="user2", point=200, solved_chall_name=chall2.chall_name)
    solved_chall3 = SolvedChallenges(id=3, chall_id=1, user_id="user3", point=100, solved_chall_name=chall1.chall_name)
    solved_chall4 = SolvedChallenges(id=4, chall_id=3, user_id="user3", point=150, solved_chall_name=chall3.chall_name)

    # add the test data to the session
    session.add_all([user1, user2, user3, chall1, chall2, chall3, solved_chall1, solved_chall2, solved_chall3, solved_chall4])

    # commit the changes
    session.commit()