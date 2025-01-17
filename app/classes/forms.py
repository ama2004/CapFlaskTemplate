# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of of a class. Forms are managed by the 
# Flask-WTForms library.

from flask.app import Flask
from flask import flash
from flask_wtf import FlaskForm
from mongoengine.fields import EmailField
import mongoengine.errors
#from wtforms.fields.html5 import URLField, DateField, DateTimeField, EmailField
from wtforms.validators import URL, NumberRange, Email, Optional, InputRequired, ValidationError, DataRequired, EqualTo
from wtforms import PasswordField, StringField, SubmitField, validators, TextAreaField, HiddenField, IntegerField, SelectField, FileField, BooleanField
from app.classes.data import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])  
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        try:
            User.objects.get(username=username.data)
        except mongoengine.errors.DoesNotExist:
            flash(f"{username.data} is available.")
        else:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        try:
            User.objects.get(email=email.data)
        except mongoengine.errors.DoesNotExist:
            flash(f'{email.data} is a unique email address.')
        else:
            raise ValidationError('This email address is already in use. if you have forgotten your credentials you can try to recover your account.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class ProfileForm(FlaskForm):
    #email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    role = SelectField('Role',choices=[("Organization","Organization"),("Young Person","Young Person")])
    number = StringField('Number', validators=[DataRequired()])
    gender = SelectField('Gender',choices=[("Male","Male"),("Female","Female"),("Transgender","Transgender"),("Binary","Binary"),("Nonbinary","Nonbinary"), ("Other", "Other"), ("N/A or prefer not to disclose" ,"N/A or prefer not to disclose")])
    race = SelectField('Race',choices=[("White","White"),("Black or African American","Black or African American"),("Asian","Asian"),("American Indian or Alaska Native","American Indian or Alaska Native"),("Native Hawaiian or Other Pacific Islander","Native Hawaiian or Other Pacific Islander"), ("Other", "Other"), ("N/A or prefer not to disclose", "N/A or prefer not to disclose")])
    education = SelectField('Education',choices=[("Middle School" , "Middle School"), ("High School","High School"),("College","College"), ("N/A", "N/A")])
    stem = SelectField('STEM',choices=[("Science","Science"),("Technology","Technology"),("Engineering","Engineering"),("Math","Math"),("Undecided","Undecided")])
    mentorship = SelectField('Mentorship',choices=[("Yes","Yes"),("No","No")])
    image = FileField("Image") 
    submit = SubmitField('Post')

class PostForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    goal = TextAreaField('Goal', validators=[DataRequired()])
    rating = SelectField('Rating',choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5")])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Post')

class Organization(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Post', validators=[DataRequired()])
    goal = TextAreaField('Goal', validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Organization')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')


#attempt
class OrganizationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    website = TextAreaField('Website', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired()])
    keywords = TextAreaField('Keywords', validators=[DataRequired()])
    mentorship = SelectField('Mentorsip',choices=[("Yes","Yes"),("No","No")])
    submit = SubmitField('Post')