from flask import Flask, request, redirect, render_template, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Never_tell'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.get('/')
def get_home():
    """Get to user list page(will change)"""
    users = db.session.query(User.first_name,User.last_name, User.id).all()
    
    return render_template("user_list.html", users=users)

@app.get('/users')
def get_users():
    """Get to user list page"""

    users = db.session.query(User.first_name,User.last_name, User.id).all()

    return render_template("user_list.html", users=users)

@app.get("/users/new")
def get_new_user_form():
    """Get new user form"""
    return render_template("new_user_form.html")

@app.post("/users/new")
def get_new_user_info():
    """Get new user info from form TODO: simplify if-else statement"""
    image_url = request.form["url"]
    if image_url == "":
        new_user = User(first_name=request.form["first_name"],
                    last_name=request.form["last_name"])
    else:
        new_user = User(first_name=request.form["first_name"],
                    last_name=request.form["last_name"],
                    image_url=request.form["url"])        

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.get("/users/<int:user_id>")
def get_user_details(user_id):
    """Show the info of selected user"""
    selected = User.query.get_or_404(user_id)

    return render_template("user_detail.html", user=selected)
    

@app.get("/users/<int:user_id>/edit")
def get_edit_user_info(user_id):
    """Get user info edit form"""
    user = User.query.get_or_404(user_id)

    return render_template("user_edit.html", user=user)

@app.post("/users/<int:user_id>")
def change_user_details(user_id):
    """Get back to user detail with updates"""
    user = User.query.get_or_404(user_id)
    user.first_name=request.form["first_name"]
    user.last_name=request.form["last_name"]
    user.image_url=request.form["url"]
    db.session.commit()

    return redirect("/users")

@app.post("/delete_user/<int:user_id>")
def delete_user(user_id):
    """Deletes user from database and redirect to user list page"""
    delete_user = User.query.get_or_404(user_id)
    db.session.delete(delete_user)
    db.session.commit()

    return redirect("/users")

