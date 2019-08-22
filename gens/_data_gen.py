from catalog.models import User
from catalog import db, create_app

app = create_app()

with app.app_context():
    db.create_all()
    user = User(first_name='Hello', last_name='World', email='hello.world@email.com', password='password')
    db.session.add(user)
    db.session.commit()

    # test
    print(User.query.all())
