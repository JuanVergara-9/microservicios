from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SagaState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50), nullable=False)
