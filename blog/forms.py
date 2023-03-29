from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo, ValidationError
from flask_ckeditor import CKEditorField
from blog.models import User


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

 
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    

class RegisterForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, name):
        user = User.query.filter_by(name=name.data)
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data)
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    # remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class CommentForm(FlaskForm):
    comment = CKEditorField("Comments", validators=[DataRequired()], render_kw={"style": "font-weight: bold;"})
    submit = SubmitField("Submit Comment")