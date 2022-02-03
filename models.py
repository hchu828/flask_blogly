from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
                            default="https://www.google.com/url?sa=i&url=https%3A%2F%2Farca.live%2Fb%2Fgenshin%2F39440165%3Fmode%3Dbest&psig=AOvVaw22i5aNM1oSAuk4Wl5ewjgi&ust=1643935779319000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCMC5ppqo4vUCFQAAAAAdAAAAABAD")
        
