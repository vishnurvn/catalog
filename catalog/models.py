from flask_login import UserMixin

from catalog import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    average_rating = db.Column(db.Float, nullable=False)
    isbn = db.Column(db.String(10), nullable=False, unique=True)
    language = db.Column(db.String(20), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    rating_count = db.Column(db.Integer, nullable=False)
    text_review_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    total_count = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '{}'.format(self.title)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    books = db.relationship('Book', backref='borrower', lazy=True)

    def __repr__(self):
        return '{}_{}'.format(self.username, 'admin' if self.is_admin else 'normal')

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
