from flaskblog import db
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from .forms import PostForm
from .models import Post
import secrets, os
from werkzeug.utils import secure_filename
from PIL import Image
from flask_login import current_user, login_required

posts_bp = Blueprint('posts_bp', __name__)




def save_thumbnail_image(image_data):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_data.filename)
    filename = secure_filename(f"{random_hex}{f_ext}")
    filepath = os.path.join(current_app.root_path, 'static/post_thumbnails')

    # Ensure the directory exists
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    full_filepath = os.path.join(filepath, filename)

    # Resize and save the image
    output_size = (300, 400)
    image = Image.open(image_data)
    image.thumbnail(output_size)
    image.save(full_filepath)

    return filename



# ad author to the model




@posts_bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title = form.title.data,
            content = form.content.data,
            user_id = current_user.id
        )
        db.session.add(new_post)
        if form.thumbnail.data:
            image_file = save_thumbnail_image(form.thumbnail.data)
            new_post.thumbnail = image_file
        db.session.commit()
        flash('New Post Created Successfully!', 'success')
        return redirect(url_for('main_bp.home'))
    return render_template('create_post.html', title='Create New Post', form=form)