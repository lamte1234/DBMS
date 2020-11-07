from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, TextField
from wtforms.validators import DataRequired, EqualTo, Length


class SearchForm(FlaskForm):
    title = StringField("Title")
    year = IntegerField("Year")
    director = StringField("Director")
    submit = SubmitField("Search")


class LoginSignupForm(FlaskForm):
    login = SubmitField("Log In")
    signup = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


class UserRating(FlaskForm):
    rating = TextField("Review")
    submit = SubmitField("Share")


