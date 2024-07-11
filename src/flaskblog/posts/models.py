from flaskblog import db
from flask_login import UserMixin
from datetime import datetime
from flaskblog.users.models import User



class Post(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    thumbnail = db.Column(db.String(30), nullable=True, default="default_thumbnail.jpg")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("posts", lazy=True))
    created_at = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return f"{self.title}"
