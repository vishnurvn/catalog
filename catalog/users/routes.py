from flask import Blueprint, render_template

from catalog.models import User, Book

users = Blueprint('users', __name__)


@users.route('/user/<string:username>')
def display_profile(username):
    user = User.query.filter_by(username=username).first()
    books = Book.query.filter_by(borrower=user).all()
    return render_template('profile.html', user_details=user, books=books)
