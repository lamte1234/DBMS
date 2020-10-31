from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SearchForm(FlaskForm):
    title = StringField('Title')
    year = StringField('Year')
    director = StringField('Director')
    submit = SubmitField('Search')