from datetime import datetime

from flask import render_template, Blueprint, jsonify, request
from flask_login import current_user

from catalog.models import Book

books = Blueprint('books', __name__)


@books.route('/get_book_list', methods=['POST'])
def get_book_list():
    page = request.json['page']
    book_list = Book.query.paginate(page=page, per_page=10)
    book_details = []
    for book in book_list.items:
        book_details.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'rating': book.average_rating,
            'availability': book.availability()
        })
    return jsonify(book_details)


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
