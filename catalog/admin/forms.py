from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from catalog.models import User


class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name')
    is_admin_check = BooleanField('Admin')
    email = StringField('Email', validators=[Email(), DataRequired()])
    submit = SubmitField('Add User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already associated with another user')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User with this username already exists')


class AddUsersForm(FlaskForm):
    users_file = FileField('File', validators=[FileField('csv')])
