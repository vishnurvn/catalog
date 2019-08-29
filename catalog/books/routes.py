from flask import render_template, Blueprint, jsonify, request
from flask_login import current_user

from catalog.exceptions import BorrowLimitExceeded
from catalog.models import Book

books = Blueprint('books', __name__)


@books.route('/get_book_list', methods=['POST'])
def get_book_list():
    page = request.json['page']
    book_list = Book.query.paginate(page=page, per_page=10)
    data = {
        'num_pages': [idx for idx in range(book_list.pages)],
    }
    book_data = []
    for book in book_list.items:
        book_data.append({
            'id': book.id,
            'title': book.title,
            'author': [author.name for author in book.author],
            'isbn': book.isbn,
            'rating': book.average_rating,
            'availability': book.availability()
        })
    data['book_data'] = book_data
    data['page_num'] = page
    return jsonify(data)


@books.route('/book/<int:book_id>')
def display_book_details(book_id):
    book = Book.query.get(book_id)
    return render_template('book.html', book=book)


@books.route('/book/<int:book_id>/borrow')
def borrow_book(book_id):
    book = Book.query.filter_by(book_id).first()
    try:
        book.borrow_book(current_user)
    except BorrowLimitExceeded:
        return jsonify({
            'status': 'error'
        })
    return jsonify({
        'status': 'ok'
    })
