from io import BytesIO
from flask import render_template, redirect, url_for, flash, abort, request, send_file
from blog import app, db, login_manager
from blog.forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, SearchForm
from blog.models import User, BlogPost, PurposePost, RelationshipPost, Fiction, Newsletter, Upload, Comment
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from bs4 import BeautifulSoup


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


# Passing searched data to the navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


# @app.route('/')
# def home():
#     page = request.args.get("page", 1, type=int)
#     posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
#     return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/')
def home():
    return render_template("about.html", current_user=current_user)


@app.route("/purpose")
def purpose():
    page = request.args.get("page", 1, type=int)
    posts = PurposePost.query.order_by(PurposePost.date.desc()).paginate(page=page, per_page=5)
    return render_template("purpose_post.html", all_posts=posts, current_user=current_user)
    

@app.route("/relationship")
def relationship():
    page = request.args.get("page", 1, type=int)
    posts = RelationshipPost.query.order_by(RelationshipPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("relationship.html", all_posts=posts, current_user=current_user)


@app.route("/fiction")
def fiction():
    page = request.args.get("page", 1, type=int)
    posts = Fiction.query.order_by(Fiction.date.desc()).paginate(page=page, per_page=5)
    return render_template("fictions.html", all_posts=posts, current_user=current_user)


@app.route("/newsletter")
def newsletter():
    page = request.args.get("page", 1, type=int)
    posts = Newsletter.query.order_by(Newsletter.date.desc()).paginate(page=page, per_page=5)
    return render_template("newletters.html", all_posts=posts)


@app.route("/my-books", methods=["GET", "POST"])
def others():
    if request.method == "POST":
        file = request.files["file"]
        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()
        return f"Uploaded: {file.filename}"
    return render_template("others.html")


@app.route("/download/<upload_id>")
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)


@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched_post = form.searched.data
        posts = BlogPost.query.filter(BlogPost.body.like("%" + searched_post + "%"))
        ordered_posts = posts.order_by(BlogPost.title).all()
        return render_template("search.html", form=form, searched=searched_post, posts=ordered_posts)


@app.route('/register', methods=["GET", "POST"]) 
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # flash(f"Account created for {form.name.data}!", "success")
        if User.query.filter_by(email=form.email.data).first():
            flash("You've already signed up with that email, log in instead!", "danger")
            return redirect(url_for("login"))
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password
        )
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again!", "danger")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash("Password Incorrect, Please try again!", "danger")
            return redirect(url_for("login"))
        else:
            login_user(user)
            next_page = request.args.get("next")
            print(next_page)
            # if next_page:
            #     return redirect(next_page)
            # # else:
            # return redirect(url_for("home"))
            # return redirect(next_page)
            return redirect(next_page) if next_page else redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def show_post(post_id):
    form = CommentForm()
    requested_post = BlogPost.query.get(post_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.", "info")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )
        db.session.add(new_comment)
        db.session.commit()
    return render_template("post.html", form=form, post=requested_post, title=requested_post.title, current_user=current_user)


@app.route("/about")
def about():
    posts = BlogPost.query.order_by(BlogPost.date.desc())
    return render_template("about.html", all_posts=posts, current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    # soup = BeautifulSoup(form.body.data, "html.parser")
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", form=form, current_user=current_user)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user,
        body=post.body
    )
    soup = BeautifulSoup(edit_form.body.data, "html.parser")
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = soup.text
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, current_user=current_user)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

