from .models import User
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flaskblog import db
from .forms import UserRegistrationForm, UserLoginForm, User_Account_Update_Form
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from PIL import Image
import os, secrets


user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/user/register', methods=['GET','POST'])
def user_register():

    if current_user.is_authenticated:
        return redirect(url_for("main_bp.home"))
    
    form = UserRegistrationForm()
    if form.validate_on_submit():

        hex_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hex_password
        )

        db.session.add(new_user)
        db.session.commit()
        flash(f'Your Account Successfully Created {form.username.data} !!!', 'success')
        return redirect(url_for('user_bp.user_login'))

    return render_template('register.html', form=form, title="Sign Up")


@user_bp.route('/login', methods=['GET','POST'])
def user_login():

    if current_user.is_authenticated:
        return redirect(url_for("main_bp.home"))
    
    form = UserLoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f"Welcome {user.username} !!!, You have successfully logged in")
            return redirect(next_page) if next_page else redirect(url_for('main_bp.home'))
        else:
            flash("Plese Enter Correct email or password !", 'warning')
        
    return render_template('login.html', form=form, title='Login')
    

@user_bp.route('/logout', methods=['GET'])
def user_logout():
    logout_user()
    return redirect(url_for('user_bp.user_login'))

@user_bp.route('/user/account')
@login_required
def user_account():
    return render_template('account.html', title='Account', current_user=current_user)






def save_profile_image(image_data):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_data.filename)
    filename = secure_filename(f"{random_hex}{f_ext}")
    filepath = os.path.join(current_app.root_path, 'static/profile_pics')

    # Ensure the directory exists
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    full_filepath = os.path.join(filepath, filename)

    # Resize and save the image
    output_size = (100, 100)
    image = Image.open(image_data)
    image.thumbnail(output_size)
    image.save(full_filepath)

    return filename


@user_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_account_edit(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        flash('You can only edit your own account!', 'danger')
        return redirect(url_for('main_bp.home'))
    
    form = User_Account_Update_Form()

    if form.validate_on_submit():
        if form.username.data != user.username:
            user.username = form.username.data
        if form.email.data != user.email:
            user.email = form.email.data
        
        if form.image.data:
            # Save the profile image
            image_file = save_profile_image(form.image.data)
            user.profile_pic = image_file
        
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user_bp.user_account', user_id=user.id))
    
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    
    return render_template('account_edit.html', title='Account Edit', form=form)