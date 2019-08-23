import csv
import random
import os

from catalog.models import User, Book
from catalog import db, create_app, bcrypt

app = create_app()

parent_folder_path = os.path.dirname(os.path.dirname(__file__))
data_path = os.path.dirname(__file__)
db_path = os.path.join(parent_folder_path, 'catalog')
user_data = 'MOCK_DATA.csv'
book_data = 'books.csv'
review_data = 'review.txt'

if 'site.db' in os.listdir('./catalog'):
    os.remove(os.path.join(db_path, 'site.db'))

with app.app_context():
    db.create_all()
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

    with open(os.path.join(data_path, book_data), 'r') as file:
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
            book = Book(**row, total_count=random.randint(1, 5), description=description)
            db.session.add(book)
            db.session.commit()

    print(len(User.query.all()))
    print(len(Book.query.all()))
