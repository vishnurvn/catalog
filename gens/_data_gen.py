import csv
import random
import os

from catalog.models import User, Book
from catalog import db, create_app

app = create_app()

if 'site.db' in os.listdir('../catalog'):
    os.remove('../catalog/site.db')

with app.app_context():
    db.create_all()
    with open('./MOCK_DATA.csv') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:
            # noinspection PyArgumentList
            user = User(**row, is_admin=False)
            db.session.add(user)
            db.session.commit()
        # noinspection PyArgumentList
        user = User(first_name='Jon', last_name='Don', email='jon.don@email.com', username='jon.don',
                    password='password', is_admin=True)
        db.session.add(user)
        db.session.commit()

    with open('./books.csv', 'r') as file:
        csv_reader = csv.DictReader(file, delimiter=',')
        for row in csv_reader:

            with open('./review.txt') as review_file:
                review = review_file.read()[0:random.randint(100, 1000)]

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
            book = Book(**row, total_count=random.randint(1, 5), review=review)
            db.session.add(book)
            db.session.commit()

    print(len(User.query.all()))
    print(len(Book.query.all()))
