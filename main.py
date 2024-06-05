import os
from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# this app variable needs to be defined as is in the main.py for Google Cloud Run
app = Flask(__name__)
# define database instance
db = SQLAlchemy()
# this requires a DATABASE_URI environment variable which we'll define in a sec
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
# library that handles migrations https://flask-migrate.readthedocs.io/en/latest/
migrate = Migrate(app, db, compare_type=True)
db.init_app(app)

# super basic user model
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(60))

@app.route("/")
def render_home_page():
    users = User.query.all()
    # return index.html template (we'll fill this in next)
    return render_template("index.html", users=users)

# Serves as a basic handler for a create user form
@app.route("/users", methods=['POST'])
def create_user():
    name = request.form.get("name")
    email = request.form.get("email")

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()

    return redirect("/")

# Google Cloud Run also needs this bit of code to bootstrap the application
# https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))