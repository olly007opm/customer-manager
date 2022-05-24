from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


# Login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get fields from form
        email = request.form.get('email')
        password = request.form.get('password')

        # Checks for the user in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # Checks user password
            if check_password_hash(user.hash, password):
                # Logs in user and redirects to the home page
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='warning')
        else:
            flash('Email does not exist.', category='warning')

    return render_template("login.html", user=current_user)


# Logout page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
