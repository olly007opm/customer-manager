from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from werkzeug.security import generate_password_hash
from flask_login import current_user
from app import db
import re

admin = Blueprint('admin', __name__)


# Admin page
@admin.route('/')
def panel():
    # Ensure user is admin
    if current_user.is_authenticated and current_user.admin:
        users = User.query.all()
        return render_template("admin.html", user=current_user, users=users)

    # If the user is not admin but is authenticated, redirect to home page
    elif current_user.is_authenticated:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('views.home'))

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))


# Add a new user
@admin.route('/add-user', methods=['POST'])
def adduser():
    # Ensure user is admin
    if current_user.is_authenticated and current_user.admin:
        # Get fields from form
        email = request.form.get('email')
        name = request.form.get('name')
        is_admin = True if request.form.get('isAdmin') == "on" else False
        password = request.form.get('password')

        # Validate user information
        email_regex = re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d-]+(\.[A-Z|a-z]{2,})+')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exists.', category='warning')
        elif not re.fullmatch(email_regex, email):
            flash('Invalid email.', category='warning')
        elif len(password) < 7:
            flash('Password must be at least 8 characters.', category='warning')
        else:
            # Creates new user in the database
            new_user = User(
                email=email,
                hash=generate_password_hash(password, method='sha256'),
                name=name,
                admin=is_admin
            )
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully.', category='success')
        return redirect(url_for('admin.panel'))

    # If the user is not admin but is authenticated, redirect to home page
    elif current_user.is_authenticated:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('views.home'))

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))


# Edit user
@admin.route('/edit-user', methods=['POST'])
def edituser():
    # Ensure user is admin
    if current_user.is_authenticated and current_user.admin:
        id = int(request.form.get('id'))
        user = User.query.filter_by(id=id).first()

        user.name = request.form.get('name')
        user.email = request.form.get('email')

        if request.form.get('password'):
            user.hash = generate_password_hash(request.form.get('password'), method='sha256')
        if id == 1 or request.form.get('admin'):
            user.admin = True
        else:
            user.admin = False

        db.session.add(user)
        db.session.commit()

        flash('User updated successfully.', category='success')
        return redirect(url_for('admin.panel'))

    # If the user is not admin but is authenticated, redirect to home page
    elif current_user.is_authenticated:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('views.home'))

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))


# Delete user
@admin.route('/delete-user/<id>')
def deleteuser(id):
    # Ensure user is admin
    if current_user.is_authenticated and current_user.admin:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

        flash('User deleted successfully.', category='success')
        return redirect(url_for('admin.panel'))

    # If the user is not admin but is authenticated, redirect to home page
    elif current_user.is_authenticated:
        flash('You do not have permission to access this page.', category='danger')
        return redirect(url_for('views.home'))

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))
