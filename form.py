from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField


class SearchForm(FlaskForm):
    title = StringField("Title")
    year = IntegerField("Year")
    director = StringField("Director")
    submit = SubmitField("Search")


class LoginSignupForm(FlaskForm):
    login = SubmitField("Login")
    signup = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class SignUpForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Sign up")



