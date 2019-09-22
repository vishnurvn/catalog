from flask import render_template, Blueprint, jsonify, request, flash, redirect, url_for
from flask_login import login_required

from catalog import bcrypt, db
from catalog.admin.forms import AddUserForm, AddUsersForm
from catalog.admin.utils import random_password_generator
from catalog.models import User, Book, Author

admin = Blueprint('admin', __name__)


@login_required
@admin.route('/api/admin/get_users/<int:page>')
def display_users(page):
    users = User.query.paginate(page=page, per_page=10)
    master_data = {}
    data = [{
        'id': user.id,
        'Username': user.username,
        'Name': user.full_name,
        'Email': user.email,
        'Admin': 'Yes' if user.is_admin else 'No'
    } for user in users.items]
    master_data['data'] = data
    master_data['num_pages'] = [idx for idx in range(users.pages)]
    return jsonify(master_data)


@admin.route('/api/admin/get_books/<int:page>')
@login_required
def display_books(page):
    master_data = {}
    books = Book.query.paginate(page=page, per_page=10)
    data = [{
        'id': book.id,
        'Title': book.title,
        'ISBN': book.isbn
    } for book in books.items]
    master_data['data'] = data
    master_data['num_pages'] = [idx for idx in range(books.pages)]
    return jsonify(master_data)


@admin.route('/admin')
@admin.route('/admin/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html', title='Dashboard')


@admin.route('/admin/database/users')
@login_required
def database_users():
    try:
        page = int(request.args['page'])
    except KeyError:
        page = 1
    users = User.query.paginate(page=page, per_page=10)
    page_num = users.pages
    form = AddUserForm()
    return render_template('admin/admin_users.html', users=users, form=form, page_num=page_num)


@admin.route('/admin/database/books')
@login_required
def database_books():
    try:
        page = int(request.args['page'])
    except KeyError:
        page = 1
    books = Book.query.paginate(page=page, per_page=10)
    page_num = books.pages
    form = AddUserForm()
    return render_template('admin/admin_books.html', books=books, form=form, page_num=page_num)


@admin.route('/admin/database/authors')
@login_required
def database_authors():
    try:
        page = int(request.args['page'])
    except KeyError:
        page = 1
    authors = Author.query.paginate(page=page, per_page=10)
    page_num = authors.pages
    form = AddUserForm()
    return render_template('admin/admin_authors.html', authors=authors, form=form, page_num=page_num)


@admin.route('/admin/database/add_user', methods=['POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        password = random_password_generator()
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # noinspection PyArgumentList
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hashed_password,
            is_admin=form.is_admin_check.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User successfully added.', category="success")
    return redirect(url_for('admin.database_users'))


@admin.route('/admin/database/delete_users', methods=['POST'])
@login_required
def delete_users():
    user_ids = request.form.getlist('user')
    if len(user_ids) == 0:
        flash('No users selected for deletion', category="warning")
        return redirect(url_for('admin.database_users'))
    for idx in user_ids:
        user = User.query.get(int(idx))
        db.session.delete(user)
        db.session.commit()
    flash('User(s) successfully deleted', category="success")
    return redirect(url_for('admin.database_users'))


@admin.route('/admin/databases/add_bulk_user')
@login_required
def add_bulk_user():
    form = AddUsersForm()
    pass


def update_user_permissions():
    pass


def add_book():
    pass


def add_bulk_books():
    pass


def delete_book():
    pass
