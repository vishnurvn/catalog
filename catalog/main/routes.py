from flask import render_template, Blueprint, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user

from catalog import db, bcrypt
from catalog.models import User, Book
from catalog.users.forms import LoginForm, RegistrationForm

main = Blueprint('main', __name__)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            # noinspection PyArgumentList
            user = User(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hashed_password,
                is_admin=False
            )
            db.session.add(user)
            db.session.commit()
            message = 'User successfully created'
            return redirect(url_for('main.login', messages=message))
        flash('User already exist')
    return render_template('form.html', form=form)


@main.route('/')
@main.route('/home')
def home():
    book_list = Book.query.limit(10).all()
    return render_template('home_page.html', current_user=current_user, book_list=book_list)
