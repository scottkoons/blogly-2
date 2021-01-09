from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

########## Models ##########


class User(db.Model):
    """User."""

    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url={u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False,
                           )
    last_name = db.Column(db.String(50),
                          nullable=False,
                          )
    image_url = db.Column(db.String(
        200))

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")


class Post(db.Model):
    """Post."""

    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<Post id={p.id}, title={p.title}, content={p.content}, created_at={p.created_at}, users_id={p.users_id}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user_post = db.relationship(
        'User', backref='post')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):
    """Post Tag models"""
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tags for posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )
