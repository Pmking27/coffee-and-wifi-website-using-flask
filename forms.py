from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, EmailField, PasswordField, BooleanField


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[validators.DataRequired(),
                                            validators.Length(min=8, max=50),
                                            validators.Email()])
    password = PasswordField('Password', validators=[
                             validators.DataRequired(), validators.Length(min=4, max=50)])
    submit_button = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
                       validators.DataRequired(), validators.Length(min=8, max=50)])
    email = EmailField('Email', validators=[validators.DataRequired(),
                                            validators.Length(min=8, max=50),
                                            validators.Email()])
    password = PasswordField('Password', validators=[
                             validators.DataRequired(), validators.Length(min=8, max=50)])
    submit_button = SubmitField('Register')


class NewCafeForm(FlaskForm):
    name = StringField('Name', validators=[
                       validators.DataRequired(), validators.Length(min=1, max=250)])
    map_url = StringField('Map URL', validators=[
                          validators.DataRequired(), validators.Length(min=4, max=250)])
    img_url = StringField('Image URL', validators=[
                          validators.DataRequired(), validators.Length(min=4, max=250)])
    location = StringField('Location', validators=[
                           validators.DataRequired(), validators.Length(min=4, max=250)])
    has_sockets = BooleanField('Sockets')
    has_toilet = BooleanField('Toilet')
    has_wifi = BooleanField('Wifi')
    can_take_calls = BooleanField('Take Calls')
    seats = StringField('Seats', validators=[
                        validators.Length(min=1, max=250)])
    coffee_price = StringField('Coffee Price', validators=[
                               validators.DataRequired(), validators.Length(min=1, max=250)])
    submit_button = SubmitField('Submit')                    
