from datetime import timedelta, datetime

from flask_login import UserMixin

from catalog import db, login_manager
from catalog.exceptions import BorrowLimitExceeded


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


author_mapping = db.Table(
    'author_mapping',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    average_rating = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.String(10), nullable=False, unique=True)
    language = db.Column(db.String(20), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    text_review_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    total_count = db.Column(db.Integer, nullable=False)
    is_borrowed = db.Column(db.Boolean, unique=False, default=False)
    borrowed_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('Author', secondary=author_mapping, backref=db.backref('book', lazy='dynamic'))

    def __repr__(self):
        return '{}'.format(self.title)

    def next_available(self):
        return (self.borrowed_date + timedelta(days=3)).date()

    def availability(self):
        return 'Unavailable' if self.is_borrowed else 'Available'

    def borrow_book(self, user):
        if user.num_borrowed_books >= user.BORROW_LIMIT:
            raise BorrowLimitExceeded('Borrow limit exceeded')
        self.is_borrowed = True
        self.borrower = user
        self.borrowed_date = datetime.now()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class User(db.Model, UserMixin):
    BORROW_LIMIT = 4
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    books = db.relationship('Book', backref='borrower', lazy=True)
    num_borrowed_books = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '{}_{}'.format(self.username, 'admin' if self.is_admin else 'normal')

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
