from flask import render_template, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user

from catalog import bcrypt
from catalog.models import User
from catalog.users.forms import LoginForm

admin = Blueprint('admin', __name__)


@admin.route('/admin/users')
def display_users():
    if current_user.is_admin:
        user_list = User.query.all()
        return render_template('admin/user_list.html', user_list=user_list)
    return redirect(url_for('main.home'))


@admin.route('/admin/', methods=['GET', 'POST'])
@admin.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated and current_user.is_admin:
        redirect(url_for('admin.admin_dash'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            abort(403)
        else:
            if user.is_admin and bcrypt.check_password_hash(user.password, form.password.data):
                redirect(url_for('admin.admin_dash'))
            else:
                flash('Login unsuccessful. Check your username or password', 'danger')
    return render_template('admin/login.html', form=form)


@admin.route('/admin/home')
def admin_dash():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return render_template('admin/home.html')
        else:
            return render_template(url_for('errors.error_403'))
    else:
        redirect(url_for('admin.login_admin'))


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
