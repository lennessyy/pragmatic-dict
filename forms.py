from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms import StringField, PasswordField, TextAreaField
from models import User, Search, db
from wtforms.validators import InputRequired

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class UserForm(ModelForm):
    class Meta:
        model = User

class NoteForm(FlaskForm):
    note = TextAreaField('Notes to make on the search', validators=[InputRequired()])

class LoginForm(FlaskForm):
    '''Login form'''
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])