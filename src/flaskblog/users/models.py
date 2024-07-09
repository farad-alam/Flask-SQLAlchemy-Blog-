from flaskblog import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(130), nullable=False, unique=True)
    password = db.Column(db.String(70), nullable=False )
    profile_pic = db.Column(db.String(30), nullable=True, default='default_profile.png')
    created_at = db.Column(db.DateTime, default=datetime.now())



    def __repr__(self):
        return f"{self.username} - {self.email} - {self.created_at}"