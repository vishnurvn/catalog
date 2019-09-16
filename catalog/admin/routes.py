from flask import render_template, Blueprint, redirect, url_for, jsonify
from flask_login import current_user, login_required

from catalog.models import User, Book
from catalog.users.forms import LoginForm, RegistrationForm

admin = Blueprint('admin', __name__)


@admin.route('/admin/users/<int:page>')
def display_users(page):
    users = User.query.paginate(page=page, per_page=10)
    return jsonify([{
        'Username': user.username,
        'Name': user.full_name,
        'Email': user.email,
        'Admin': 'Yes' if user.is_admin else 'No'
    } for user in users.items])


@admin.route('/admin/books/<int:page>')
def display_books(page):
    books = Book.query.paginate(page=page, per_page=10)
    return jsonify([{
        'Title': book.title,
        'ISBN': book.isbn
    } for book in books.items])


@login_required
@admin.route('/admin/home')
def admin_home():
    login_form = LoginForm()
    registration_form = RegistrationForm
    if current_user.is_authenticated:
        if current_user.is_admin:
            return render_template('admin/home.html', login_form=login_form, registration_form=registration_form)
        else:
            return render_template(url_for('errors.error_403'))
    else:
        return redirect(url_for('main.home'))


def add_user():
    pass


def add_bulk_user():
    pass


def delete_user():
    pass


def update_user_permissions():
    pass


def add_book():
    pass


def add_bulk_books():
    pass


def delete_book():
    pass
