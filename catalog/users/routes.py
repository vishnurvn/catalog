from flask import Blueprint, render_template


users = Blueprint('users', __name__)


@users.route('/home')
def home():
    return render_template('home_page.html')


@users.route('/profile/user')
def display_profile():
    return render_template('profile.html')
