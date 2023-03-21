from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, URL, Email, Length, EqualTo
from flask_ckeditor import CKEditorField

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


class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    # remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class CommentForm(FlaskForm):
    comment = CKEditorField("Comments", validators=[DataRequired()], render_kw={"style": "font-weight: bold;"})
    submit = SubmitField("Submit Comment")