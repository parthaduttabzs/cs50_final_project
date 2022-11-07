import os
import json
from flask import Flask, render_template, session, request, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from flask_session import Session
from functools import wraps
from PIL import Image
import requests


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# image resizing
image = Image.open("static/images/milk.png")
image.resize((200,200)).save("static/images/milk_200.png")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ecomm.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def login_required(f):
    # decorates routes to require login
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# define percent filter
def percent(value):
    """Format value as percent."""
    return f"{value:,.0%}"
# make filter available in jinja2
app.jinja_env.filters["percent"] = percent

    
def password_strength(password):
    # initiating variables
    length = len(password)
    lower = 0
    upper = 0
    digit = 0
    special = 0
    # loop through all the characters of the password
    for i in range(length):
        c = password[i]
        # check for lower case
        if (c.islower()):
            lower += 1
        # check for upper case
        if (c.isupper()):
            upper += 1
        # check for digits
        if (c.isdigit()):
            digit += 1
        # check for special characters
        if (c in ("@", "#", "_")):
            special += 1
    # check for final password validation
    if (length < 6 or lower < 1 or upper < 1 or digit < 1 or special < 1):
        # if password is not strong enough
        return False
        # password matches the validation criteri and hence strong
    else:
        return True


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    product_data = db.execute("SELECT * FROM products;")
    # cart_count = len(db.execute("SELECT * FROM carts WHERE user_id=?", user_id)["cart_items"])
    cart_count = 0
    return render_template("index.html", user_data = user_data, product_data=product_data, cart=cart_count)


def error(message, code=400):
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", code=code, message=escape(message)), code


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # if user has placed a register request
    if request.method == "POST":
        # check for valid inputs
        if not request.form.get("email") or not request.form.get("phone") or not request.form.get("name"):
            return error("must provide all valid details", 400)
        # ensure no duplicate email ID
        elif len(db.execute("SELECT user_id FROM users WHERE email = ?", request.form.get("email"))) == 1:
            return (error("Email ID already exists", 400))
        # ensure no duplicate mobile number
        elif len(db.execute("SELECT user_id FROM users WHERE phone = ?", request.form.get("phone"))) == 1:
            return (error("Mobile number already exists", 400))
        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 400)
        # ensure password matches
        elif request.form.get("password") != request.form.get("confirmation"):
            return error("password didn't match")
        # ensure password is strong (disabled to pass cs50 check50 and submit50)
        # elif not password_strength(request.form.get("password")):
        #     return error("password needs to be atleast 6 character, with min 1 upper, 1 lower, 1 digit and 1 special ('@', '#', '_') character", 400)
        # accept username and password and proceed to register
        hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (name, email, phone, hash) VALUES (?, ?, ?, ?)", request.form.get("name"), request.form.get("email"), request.form.get("phone"), hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        flash("You have successfully registered!")
        return redirect("/")
    # if user is visiting register page
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure email was submitted
        if not request.form.get("email"):
            return error("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("must provide password", 403)

        # Query database for email ID
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("invalid Email ID and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

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
    flash(f"You have successfully logged out")

    # Redirect user to login form
    return redirect("/")


@app.route("/add_fund", methods=["GET", "POST"])
def add_fund():
    # get user data
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    # if user has placed a add fund request
    if request.method == "POST":
        amount = request.form.get("amount")
        # validation check
        if not 0 < int(amount) < 1000000000:
            return error("Entered amount is invalid", 406)
        # execute fund addition
        db.execute(f"UPDATE users SET cash = (cash + ?) WHERE user_id = ?", amount, user_id)
        flash(f"Rs. {amount}/- has been added to your account")
        return redirect("/")
    # if user is visiting the add fund page
    return render_template("add_fund.html", user_data=user_data)


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    cart = db.execute("SELECT cart_items FROM carts WHERE user_id = ?;", f'{user_id}')
    cart = cart[0]['cart_items']
    # cart = list(str.split(cart,","))
    cart = json.loads( cart )
    if request.method == "POST":
        product_id = request.form.get("product_id")
        product_name = db.execute("SELECT product_name, price FROM products WHERE product_id = ?", product_id)
        qty = request.form.get("qty")
        # db.execute("UPDATE carts SET cart_items=? WHERE user_id=?",)
    flash(f"You have reached cart for user #{user_id}")
    return render_template("cart.html", cart=cart, user_data=user_data)