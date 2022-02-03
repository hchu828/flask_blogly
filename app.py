from flask import Flask, request, redirect, render_template, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Never_tell'

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def get_home():
    """Get to user list page(will change)"""
    users = db.session.query(User.first_name,User.last_name).all()
    return render_template("user_list.html", users=users)

@app.get('/users')
def get_users():
    """Get to user list page"""

    users = db.session.query(User.first_name,User.last_name).all()
    return render_template("user_list.html", users=users)



