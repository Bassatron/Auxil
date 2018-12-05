import os

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
import json
import smtplib
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

os.environ["PASSWORD"] = "C$50final"
key = "AIzaSyBkCiOOMfxTvts1TR6rKNHU3KS7RNKTWAs"

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///auxil.db")


@app.route("/", methods=["GET", "POST"])
def index():

    # POST
    if request.method == "POST":

        # Query database for zip codes
        search = request.form.get("search").title()
        zipcode = request.form.get("search")
        shortzip = zipcode[0:3]

        if not search:
            return redirect("/explore")

        organizations = db.execute("SELECT * FROM Organizations WHERE Location = :city", city=search)
        organizations2 = db.execute("SELECT * FROM Organizations WHERE Zip LIKE :shortzip", shortzip=shortzip+"%")
        if not organizations and not organizations2:
            return apology("No volunteering locations match your preferences")
        return render_template("results.html", organizations = organizations, organizations2 = organizations2)

    # GET
    else:
        return render_template("index.html")


@app.route("/explore")
@login_required
def explore():
    """Explore a map"""

    return render_template("explore.html", key = key)

@app.route("/marker")
def marker():

    # Pull marker from database
    data = db.execute("SELECT Name, Website, lat, lng, type FROM Organizations")

    # write marker data into json format
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    return redirect("/explore")


@app.route("/organizations")
def organizations():
    """All Organizations"""
    # Displays all organizations registered
    organizations = db.execute("SELECT * FROM Organizations")
    return render_template("organizations.html", organizations = organizations)

@app.route("/comment", methods=["GET", "POST"])
@login_required
def comment():
    if request.method == "POST":

        email = request.form.get("email")
        comment = request.form.get("comment")
        # Ensure all informaiton  was submitted
        if not email:
            return apology("Must provide an email", 400)
        if not comment:
            return apology("Must write an comment", 400)

        # Add comment to the forum table
        db.execute("INSERT INTO forum (Email, Comment, Time) VALUES(:email, :comment, :time)", email=email, comment=comment, time=str(datetime.now().strftime("%m-%d-%y")))
        # Send to the page with all the comments
        forum = db.execute("SELECT * FROM forum")
        return render_template("community.html", forum = forum)

    else:
         # Send to page where you can submit comments
        return render_template("comment.html")

@app.route("/community")
def community():
    """All comments"""
    # Displays all organizations registered
    forum = db.execute("SELECT * FROM forum")
    return render_template("community.html", forum = forum)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add organizations"""

    # for form submission
    if request.method == "POST":

        organization = request.form.get("organization")
        location = request.form.get("location")
        zipcode = request.form.get("zip")
        website = request.form.get("website")
        description = request.form.get("description")
        # Ensure all informaiton  was submitted
        if not organization:
            return apology("Must provide an organization", 400)
        if not location:
            return apology("Must provide an location", 400)
        if not website:
            return apology("Must provide an website", 400)
        if not description:
            return apology("Must provide an description", 400)
        if not zipcode:
            return apology("Must provide an zipcode", 400)

        # Add organization to the organizations table
        db.execute("INSERT INTO Organizations (Name, Location, Zip, Description, Website) VALUES(:organization, :location, :zipcode, :description, :website)",
                   organization=organization, zipcode=zipcode, description=description, website=website, location=location)

        # Send to page with list of all organizations
        return render_template("organizations.html")

    # For GET route
    else:
        return render_template("add.html")

@app.route("/apply", methods=["GET", "POST"])
@login_required
def apply():
    """Apply to Organizations"""

    # for form submission
    if request.method == "POST":

        organization = request.form.get("organization")
        first = request.form.get("first")
        last = request.form.get("last")
        username = request.form.get("username")
        weekdays = request.form.get("weekdays")
        weekends = request.form.get("weekends")
        night = request.form.get("night")
        day = request.form.get("day")
        reason = request.form.get("reason")
        # Ensure all informaiton  was submitted
        if not organization:
            return apology("Must provide an organization", 400)
        if not first:
            return apology("Must provide a first name", 400)
        if not last:
            return apology("Must provide a last name", 400)
        if not username:
            return apology("Must provide an email", 400)
        if not reason:
            return apology("Must answer all questions", 400)
            # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :username",
                          username=request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1:
            return apology("invalid email address", 403)
        if not last:
            return apology("Must provide a last name", 400)
        # Add organization to the organizations table
        db.execute("INSERT INTO applications (firstname, lastname, organization, username, reason, weekdays, weekends, night, day) VALUES(:first, :last, :organization, :username, :reason, :weekdays, :weekends, :night, :day)",
                   organization=organization, first=first, last=last, username=username, weekdays=weekdays, weekends=weekends, night=night, day=day, reason=reason)

        data = db.execute("SELECT * FROM applications WHERE username = :username", username=username)

        # Send to page to review application
        return render_template("completed.html")

    # For GET route
    else:
        organizations = db.execute("SELECT Name FROM Organizations")
        return render_template("apply.html", organizations = organizations)

### ### ### ### ### ### ### ### ###
###  USER LOG IN/SIGN UP STUFF  ###
### ### ### ### ### ### ### ### ###


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign users up"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure first name was submitted
        if not request.form.get("firstname"):
            return render_template("signup.html")

        # Ensure last name was submitted
        elif not request.form.get("lastname"):
            return render_template("signup.html")

        # Ensure email was submitted
        elif not request.form.get("email"):
            return render_template("signup.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("signup.html")

        elif len(request.form.get("password")) < 6:
            return apology("Password must be at least 6 characters")

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords do not match")

        registered = db.execute("INSERT INTO users (firstname, lastname, email, hash) VALUES (:firstname, :lastname, :email, :passhash)",
                                firstname=request.form.get("firstname"), lastname=request.form.get("lastname"),
                                email=request.form.get("email"), passhash=generate_password_hash(request.form.get("password")))

        if not registered:
            return apology("Email is already in use")

        # Remember who is logged in
        session["user_id"] = registered

        # Email user that they have signed up
        firstname = request.form.get("firstname")
        email = request.form.get("email")
        message = "Hi " + firstname + ", welcome to the Auxil Community!"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("teamauxil@gmail.com", os.getenv("PASSWORD"))
        server.sendmail("teamauxil@gmail.com", email, message)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("Please enter your email", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please enter password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    """Change Password"""

    # User reached via POST
    if request.method == "POST":

        row = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        if not check_password_hash(row[0]["hash"], request.form.get("oldpassword")):
            return apology("Incorrect Old Password!", 400)

        # Check new passwords
        elif not request.form.get("newpassword"):
            return apology("Must provide password", 400)

        elif len(request.form.get("newpassword")) < 6:
            return apology("Password must be at least 6 characters")

        elif request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        newhash = generate_password_hash(request.form.get("newpassword"))

        # Update hash in user table
        update = db.execute("UPDATE users SET hash = :newhash WHERE id = :id", newhash=newhash, id=session["user_id"])

        # Remember who is logged in
        session["user_id"] = update

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("change.html")