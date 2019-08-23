from datetime import datetime

from flask import render_template, Blueprint, jsonify
from flask_login import current_user

from catalog.models import Book

books = Blueprint('books', __name__)


@books.route('/book/<int:book_id>')
def display_book_details(book_id):
    book = Book.query.get(book_id)
    return render_template('book.html', book=book)


@books.route('/book/<int:book_id>/borrow')
def borrow_book(book_id):
    book = Book.query.filter_by(book_id).first()
    book.borrower = current_user
    book.is_borrowed = True
    book.borrowed_date = datetime.now()
    return jsonify({
        'status': 'OK'
    })
