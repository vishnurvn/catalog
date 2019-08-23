from flask import render_template, Blueprint

from catalog.models import Book

books = Blueprint('books', __name__)


@books.route('/book/<int:book_id>')
def display_book_details(book_id):
    book = Book.query.get(book_id)
    return render_template('book.html', book=book)
