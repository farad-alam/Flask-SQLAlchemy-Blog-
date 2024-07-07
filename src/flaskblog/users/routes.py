from .models import User
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flaskblog import db
from .forms import UserRegistrationForm, UserLoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user



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