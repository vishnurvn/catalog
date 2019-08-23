from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from catalog.models import User, Book

users = Blueprint('users', __name__)


@users.route('/users')
def display_users():
    if current_user.is_admin:
        user_list = User.query.all()
        return render_template('admin/user_list.html', user_list=user_list)
    return redirect(url_for('main.home'))


@users.route('/user/<string:username>')
def display_profile(username):
    user = User.query.filter_by(username=username).first()
    books = Book.query.filter_by(borrower=user).all()
    return render_template('profile.html', user_details=user, books=books)
