from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    db_name = StringField('Database Name', validators=[DataRequired()], default='dbbooks')
    user = StringField('User', validators=[DataRequired()], default='postgres')
    password = PasswordField('Password', validators=[DataRequired()])
    host = StringField('Host', validators=[DataRequired()], default='localhost')
    port = StringField('Port', validators=[DataRequired()], default='5432')
    submit = SubmitField('login')
    
