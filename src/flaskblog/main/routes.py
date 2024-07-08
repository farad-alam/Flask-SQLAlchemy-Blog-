from flask import Blueprint, render_template, flash
from flaskblog.posts.models import Post
from flaskblog import db


main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/')
def home():
    published_post = Post.query.all()
    return render_template('home.html', title="Flask Blog - Home", published_post=published_post)