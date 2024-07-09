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


@posts_bp.route('/post-details/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post_details.html', title=f"{post.title}", post=post, current_user=current_user)


@posts_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user.id:
        flash('You can not Edit this Post','danger')
        return redirect(url_for('posts_bp.post_details', post_id=post_id))
    # form.thumbnail.data = post.thumbnail

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        print(form.content.data)
        if form.thumbnail.data:
            image_file = save_thumbnail_image(form.thumbnail.data)
            post.thumbnail = image_file
        db.session.commit()
        flash(f"Your post '{post.title}' Updated! ")
        return redirect(url_for('posts_bp.post_details', post_id=post_id))

        
    form.title.data = post.title
    form.content.data = post.content
    
    return render_template('edit_post.html', title=f"Edit - {post.title}", form=form, post=post)

@posts_bp.route('/delete-post/<int:post_id>', methods=['GET','POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.id != post.user.id:
        flash('You can not Delete this Post','danger')
        return redirect(url_for('posts_bp.post_details', post_id=post_id))
    db.session.delete(post)
    db.session.commit()
    flash('Your post deleted successfully!')
    return redirect(url_for('main_bp.home'))