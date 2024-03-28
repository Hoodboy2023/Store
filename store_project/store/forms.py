from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from store.models import User
from store.info import countries


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(message="Invalid Email address!!"), DataRequired()])
    first_name = StringField(label='First Name',validators=[Length(min=2,max=15),DataRequired()])
    last_name = StringField(label='Last Name',validators=[Length(min=2,max=15),DataRequired()])
    phone_number = StringField(label='Phone Number', validators=[Length(max=15), DataRequired()])
    country = SelectField(label='Country',choices=countries)
    address1 = StringField(label='Address 1', validators=[Length(max=30), DataRequired()])
    address2 = StringField(label='Address 2', validators=[Length(max=30), DataRequired()])
    zip_address = StringField(label='Zip',validators=[DataRequired()])
    city = StringField(label='City',validators=[Length(max=15),DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
    submit2 = SubmitField(label="Save")


class EditForm(FlaskForm):
    email_address = StringField(label='Email Address:', validators=[Email(message="Invalid Email address!!"), DataRequired()])
    first_name = StringField(label='First Name',validators=[Length(min=2,max=15),DataRequired()])
    last_name = StringField(label='Last Name',validators=[Length(min=2,max=15),DataRequired()])
    phone_number = StringField(label='Phone Number', validators=[Length(max=15), DataRequired()])
    country = SelectField(label='Country',choices=countries)
    address1 = StringField(label='Address 1', validators=[Length(max=30), DataRequired()])
    address2 = StringField(label='Address 2', validators=[Length(max=30), DataRequired()])
    zip_address = StringField(label='Zip',validators=[DataRequired()])
    city = StringField(label='City',validators=[Length(max=15),DataRequired()])
    submit2 = SubmitField(label="Save")
  
   

class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')