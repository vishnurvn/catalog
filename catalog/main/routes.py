from flask import render_template, Blueprint, request, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user

from catalog.users.forms import LoginForm, RegistrationForm
from catalog.models import User
from catalog import db

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and form.password.data == user.password:
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Check your username or password', 'danger')
    return render_template('index.html', title='Login', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if not User.query.filter_by(email=form.email.data).first():
            # noinspection PyArgumentList
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            message = 'User successfully created'
            return redirect(url_for('main.login', messages=message))
        flash('User already exist')
    return render_template('form.html', form=form)


@main.route('/home')
def home():
    return render_template('home_page.html')
