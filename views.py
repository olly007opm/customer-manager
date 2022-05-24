from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user
from app import db
from models import Member, Booking
from datetime import datetime
import random

views = Blueprint('views', __name__)


# Home page
@views.route('/')
def home():
    # Ensure user is authenticated
    if current_user.is_authenticated:
        members = Member.query.all()
        return render_template("index.html", members=members, user=current_user)

    # If the user is not authenticated, redirect to login page
    else:
        return redirect(url_for('auth.login'))


# Edit member
@views.route('/edit-member', methods=['POST'])
def editmember():
    # Ensure user is authenticated
    if current_user.is_authenticated:
        id = request.form.get('id')
        member = Member.query.filter_by(id=id).first()

        member.surname = request.form.get('surname')
        member.joined = request.form.get('joined')
        member.nights = request.form.get('nights')
        member.points = request.form.get('points')
        member.member_id = request.form.get('memberId')
        member.membership = request.form.get('membership')

        db.session.add(member)
        db.session.commit()

        flash('Member updated successfully.', category='success')
        return redirect(url_for('views.home'))

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))


# Add member
@views.route('/add-member', methods=['GET', 'POST'])
def addmember():
    # Ensure user is authenticated
    if current_user.is_authenticated:
        if request.method == 'POST':
            member = Member(
                surname=request.form.get('surname'),
                joined=request.form.get('joined') or datetime.now().year,
                nights=request.form.get('nights') or 0,
                points=request.form.get('points') or 0,
                memberId=request.form.get('memberId'),
                membership=request.form.get('membership')
            )
            db.session.add(member)
            db.session.commit()

            flash('Member added successfully.', category='success')
            return redirect(url_for('views.home'))
        else:
            # Get the next id and they year
            nextid = int(Member.query.order_by(Member.id.desc()).first().id) + 1
            year = datetime.now().year

            # Generate a random 3-digit number and pad the number with 0s if less than 100
            randomnum = random.randint(0, 999)
            if randomnum < 10:
                randomnum = "00" + str(randomnum)
            elif randomnum < 100:
                randomnum = "0" + str(randomnum)
            else:
                randomnum = str(randomnum)

            return render_template("add-member.html", nextid=nextid, randomnum=randomnum, year=year)

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))


# Delete member
@views.route('/delete-member/<id>')
def deletemember(id):
    # Ensure user is authenticated
    if current_user.is_authenticated:
        member = Member.query.filter_by(id=id).first()
        db.session.delete(member)
        db.session.commit()

        flash('Member deleted successfully.', category='success')
        return redirect(url_for('views.home'))

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))


# New booking
@views.route('/new-booking/<id>', methods=['GET', 'POST'])
def newbooking(id):
    # Ensure user is authenticated
    if current_user.is_authenticated:
        if request.method == 'POST':
            id = request.form.get('id')
            # Format the start and end dates
            startdate = datetime.strptime(request.form.get('startdate'), "%Y-%m-%d")
            enddate = datetime.strptime(request.form.get('enddate'), "%Y-%m-%d")
            # Calculate the number of nights
            nights = (enddate - startdate).days

            # Create a new booking record
            booking = Booking(
                member=id,
                start=startdate,
                end=enddate,
                nights=nights
            )
            db.session.add(booking)

            # Update the member record
            member = Member.query.filter_by(id=id).first()
            member.nights += nights
            # Calculate the points based on the member's membership
            if member.membership == "Platinum":
                member.points += nights * 4000
            elif member.membership == "Gold":
                member.points += nights * 3000
            else:
                member.points += nights * 2500

            # Check if the member's membership needs to be upgraded
            if member.nights >= 100:
                member.membership = "Platinum"
            elif member.nights >= 30 and member.membership == "Silver":
                member.membership = "Gold"
            db.session.add(member)

            db.session.commit()

            flash('Booking added successfully.', category='success')
            return redirect(url_for('views.home'))
        else:
            member = Member.query.filter_by(id=id).first()
            return render_template("new-booking.html", member=member)

    # If the user is not authenticated, redirect to login page
    else:
        flash('You need to login to access this page.', category='warning')
        return redirect(url_for('auth.login'))


# GENERAL
# redirect(url_for('views.page'))
# @login_required
# if current_user.is_authenticated:

# DATABASE
# Table.query.all()
# Table.query.filter_by( <QUERY OPTIONS> ).first()
#   <QUERY OPTIONS> id=123 name='test'
# current_user.linkedtable
# new_record = Record(field=data, field2=data2)
# db.session.add(new_record)
# db.session.commit()

# REQUESTS
# @views.route('/path', methods=['GET', 'POST'])
# if request.method == 'POST':
# request.form.get('input name')
# request.form.getlist('common input name')
