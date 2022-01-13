from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Deployment(db.Model):
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
