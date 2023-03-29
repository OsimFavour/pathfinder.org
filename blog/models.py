from blog import db
from datetime import datetime
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    purpose_posts = relationship("PurposePost", back_populates="author")
    relationship_posts = relationship("RelationshipPost", back_populates="author")
    fiction = relationship("Fiction", back_populates="author")
    newsletters = relationship("Newsletter", back_populates="author")
    books = relationship("Upload", back_populates="book_author")
    comments = relationship("Comment", back_populates="comment_author") 

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.password}')"


class PurposePost(db.Model):
    __tablename__  = "purpose_post"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    comments = relationship("Comment", back_populates="parent_post")


class RelationshipPost(db.Model):
    __tablename__ = "relationship_posts"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))    
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    comments = relationship("Comment", back_populates="parent_post")

     
class Fiction(db.Model):
    __tablename__ = "fiction_posts"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    comments = relationship("Comment", back_populates="parent_post")


    def __repr__(self):
        return f"Post('{self.author}', '{self.title}', '{self.date}')"


     
class Newsletter(db.Model):
    __tablename__ = "newsletters"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # comments = relationship("Comment", back_populates="parent_post")


    def __repr__(self):
        return f"Post('{self.author}', '{self.title}', '{self.date}')"
    

class Upload(db.Model):
    __tablename__  = "book_upload"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    book_author = relationship("User", back_populates="books")
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")

    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("PurposePost", back_populates="comments")

    
    text = db.Column(db.Text, nullable=False)


db.drop_all()
db.create_all()