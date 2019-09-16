from flask import render_template, Blueprint, jsonify, request

from catalog.models import Book
from catalog.users.forms import LoginForm

books = Blueprint('books', __name__)


@books.route('/get_book_list', methods=['POST'])
def get_book_list():
    page = request.json['page']
    # author filter
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
    login_form = LoginForm()
    return render_template('book.html', book=book, login_form=login_form)
