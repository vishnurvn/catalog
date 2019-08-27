import csv
import os
import random
from datetime import datetime

from catalog import db, create_app, bcrypt
from catalog.models import User, Book, Author

app = create_app()

parent_folder_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.dirname(__file__)
db_path = os.path.join(parent_folder_path, 'catalog')
user_data = 'MOCK_DATA.csv'
book_data = 'books.csv'
review_data = 'review.txt'


if 'site.db' in os.listdir(db_path):
    os.remove(os.path.join(db_path, 'site.db'))

with app.app_context():
    db.create_all()

    with open(os.path.join(data_path, book_data), 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        author_list = set()
        for row in csv_reader:
            authors = row['author'].split('-')
            for author in authors:
                author_list.add(author)

        for author_name in author_list:
            author = Author(name=author_name)
            db.session.add(author)
        db.session.commit()

    with open(os.path.join(data_path, user_data)) as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            row['password'] = bcrypt.generate_password_hash(row.pop('password')).decode('utf-8')
            # noinspection PyArgumentList
            user = User(**row, is_admin=False)
            db.session.add(user)
            db.session.commit()
        hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
        # noinspection PyArgumentList
        user = User(first_name='Jon', last_name='Don', email='jon.don@email.com', username='jon.don',
                    password=hashed_password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        users = User.query.all()

    with open(os.path.join(data_path, book_data), 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:

            with open(os.path.join(data_path, review_data)) as review_file:
                description = review_file.read()[0:random.randint(100, 1000)]

            pop_able_list = ['bookID', 'isbn13', '']
            for pop_able in pop_able_list:
                try:
                    row.pop(pop_able)
                except KeyError:
                    continue
            int_able_list = ['num_pages', 'rating_count', 'text_review_count']
            for int_able in int_able_list:
                row[int_able] = int(row.pop(int_able))
            row['average_rating'] = float(row.pop('average_rating'))
            borrow_book = random.choice([True, False])
            authors = row.pop('author').split('-')
            if borrow_book:
                user = random.choice(users)
                book = Book(**row, total_count=random.randint(1, 5), description=description,
                            borrower=user, is_borrowed=True, borrowed_date=datetime.now())
            else:
                book = Book(**row, total_count=random.randint(1, 5), description=description)
            for author_name in authors:
                author = Author.query.filter_by(name=author_name).first()
                book.author.append(author)

            db.session.add(book)
            db.session.commit()

    print(len(users))
    print(len(Book.query.all()))
