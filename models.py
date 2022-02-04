from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://ac-p.namu.la/20211130s1/b4f40cfe4ddd6dd15162c5e7d695fea157dae5cfadea8f2f6561ba83107848ab.png?type=orig"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


"""Models for Blogly."""

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column( db.String(50),
                            nullable=False)
    last_name = db.Column(  db.String(50),
                            nullable=False)
    image_url = db.Column(  db.String(), 
                            default=DEFAULT_IMAGE_URL)
        
class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.column(db.String(50),
                        nullable=False)
    content = db.column(db.String())
    created_at = db.column(db.Date(),
                            nullable=False)
    user_id = db.column(db.Integer,
                        db.ForeignKey('users.id'))
    users = db.relationship('User', backref='posts')