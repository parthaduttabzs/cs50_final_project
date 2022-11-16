import os
import json
from flask import Flask, render_template, session, request, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from flask_session import Session
from functools import wraps
import datetime
import requests
from PIL import Image


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ecomm.db")

# following code helps with converting the images from webp to png and resize theme to 200x200 px

# path = "static/images/webp/"
# files = os.listdir(path)
# # id = 0
# for file in files:
#     img_path = path + file
#     filename = os.path.splitext(file)[0]
#     image = Image.open(img_path).convert("RGB")
#     image.resize((200,200)).save(fr"static/images/{filename}.png","png")
    
    # print(text)
    # text = '204629_16-aashirvaad-select-atta.webp'
    # index_start = 0
    # index_end = 0
    # for i in range(0, len(text)-1, 1):
    #     if text[i].isalpha():
    #         index_start = text.find(text[i])
    #         # print(text[i])
    #         continue
    #     if text[i] == ".":
    #         index_end = text.find(text[i])
    #         break
    # text1 = text[index_start:index_end]
    # text1 = text.replace('/.webp','')
    # print(text1)
    # text3 = text2.title()
    # id += 1
    # print(text1)
    # db.execute(f"INSERT INTO product_temp VALUES('{id}','{text3}');")
    # os.remove(file)


# image = Image.open("static/images/milk.png")
# image.resize((200,200)).save("static/images/milk_200.png")



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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    product_data = db.execute("SELECT * FROM products;")
    cart = db.execute("SELECT * FROM carts WHERE user_id = ?;", user_id)
    cart_list = cart[0]['cart_items']
    cart_list = json.loads(cart_list)
    return render_template("index.html", user_data = user_data, product_data=product_data, cart=cart_list)


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
        db.execute("INSERT INTO carts (user_id, cart_items) VALUES (?,?);", session["user_id"],'[]')
        db.execute("INSERT INTO address (user_id, address, primary_address) VALUES (?,?,?);", session["user_id"],'[]', 0)
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
@login_required
def add_fund():
    # get user data
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    # if user has placed a add fund request
    if request.method == "POST":
        amount = int(request.form.get("amount"))
        # validation check
        if not 0 < amount < 1000000000:
            return error("Entered amount is invalid", 406)
        # execute fund addition
        db.execute("UPDATE users SET cash = (cash + ?) WHERE user_id = ?", amount, user_id)
        # Log transaction
        db.execute("INSERT INTO transactions (user_id, tran_type, amount, datetime, tran_status) VALUES(?,?,?,?,?);", user_id, "ADD_FUND", amount, datetime.datetime.now(), "SUCCESS")
        flash(f"Rs. {amount}/- has been added to your account")
        return redirect("/")
    # if user is visiting the add fund page
    return render_template("add_fund.html", user_data=user_data)


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    # get user data
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    # get address data of the user
    address = db.execute("SELECT address FROM address WHERE user_id= ?", user_id)
    address = address[0]['address']
    #convert address details in JSON for JINJA
    address = json.loads( address )
    # get cart data of the user
    cart = db.execute("SELECT cart_items FROM carts WHERE user_id = ?;", user_id)
    # if cart:
    cart = cart[0]['cart_items']
    # else:
    #     cart = []
    cart = json.loads( cart )
    for i in cart:
        prod = db.execute("SELECT * FROM products WHERE product_id = ?;", i["product_id"])
        i["product_name"] = prod[0]["product_name"]
        i["price"] = prod[0]["price"]
        i["image"] = prod[0]["image"]
        i["desc"] = prod[0]["desc"]
        i["amount"] = int(prod[0]["price"]) * int(i["qty"])
    return render_template("cart.html", cart=cart, user_data=user_data, address=address)


@app.route("/add_to_cart", methods=["GET", "POST"])
@login_required
def add_to_cart():
    user_id = session["user_id"]
    cart = db.execute("SELECT * FROM carts WHERE user_id = ?;", user_id)
    if request.method == "POST":
        product_id = request.form.get("product_id")
        qty = int(request.form.get("qty"))
        if qty <= 0:
            return error("Please enter valid inputs", 400)
        cart_list = cart[0]['cart_items']
        cart_json = json.loads( cart_list )
        for i in cart_json:
            if i['product_id'] == product_id:
                i['qty'] = int(i['qty']) + (qty)
                db.execute("UPDATE carts SET cart_items = ? WHERE user_id = ?;", json.dumps(cart_json), user_id)
                flash(f"Cart has been updated")
                return redirect("/")
        new = {}
        new['product_id'] = product_id
        new['qty'] = qty
        new['price'] = db.execute("SELECT price FROM products WHERE product_id = ?", product_id)[0]['price']
        cart_json.append(new)
        db.execute("UPDATE carts SET cart_items = ? WHERE user_id = ?;", json.dumps(cart_json), user_id)
        flash(f"Cart has been updated")
        return redirect("/")


@app.route("/remove_from_cart", methods=["GET", "POST"])
@login_required
def remove_from_cart():
    user_id = session["user_id"]
    cart = db.execute("SELECT cart_items FROM carts WHERE user_id = ?;", user_id)
    cart_list = cart[0]['cart_items']
    cart_json = json.loads( cart_list )
    if request.method == "POST":
        product_id = request.form.get("product_id")
        for i in cart_json:
            if i['product_id'] == product_id:
                cart_json.remove(i)
                db.execute("UPDATE carts SET cart_items = ?;", json.dumps(cart_json))
                flash(f"Item has been removed from cart")
                return redirect("/cart")
    else:
        return redirect("/cart")


@app.route("/summary", methods=["GET", "POST"])
@login_required
def summary():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    address = request.form.get('address_selected')
    if len(address) == 0:
        flash("Please select an address for delivery")
        return redirect("/cart")
    cart = db.execute("SELECT cart_items FROM carts WHERE user_id = ?;", user_id)
    if len(cart) == 0:
        flash("Please select an address for delivery")
        return redirect("/cart")
    else:
        cart_list = cart[0]['cart_items']
        cart_list = json.loads(cart_list)
        for i in cart_list:
            prod = db.execute("SELECT * FROM products WHERE product_id = ?;", i["product_id"])
            i["product_name"] = prod[0]["product_name"]
            i["price"] = prod[0]["price"]
            i["image"] = prod[0]["image"]
            i["desc"] = prod[0]["desc"]
            i["amount"] = int(prod[0]["price"]) * int(i["qty"])
    return render_template("summary.html", cart=cart_list, user_data=user_data, address=address)


@app.route("/add_address", methods=["GET", "POST"])
@login_required
def add_address():
    # get user data
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    address = db.execute("SELECT address FROM address WHERE user_id= ?", user_id)
    address = address[0]['address']
    address = json.loads( address )
    if request.method == "POST":
        source = request.form.get("source")
        new = {}
        new['address'] = request.form.get("address")
        address.append(new)
        db.execute("UPDATE address SET address = ? WHERE user_id = ?;", json.dumps(address), user_id)
        flash(f"New address has been added")
        return redirect(f"/{source}")
    source = request.args.get("source")
    return render_template("address.html", user_data=user_data, address=address, source=source)


@app.route("/delete_address", methods=["GET", "POST"])
@login_required
def delete_address():
    user_id = session["user_id"]
    address = db.execute("SELECT address FROM address WHERE user_id= ?", user_id)
    address = address[0]['address']
    address_json = json.loads( address )
    if request.method == "POST":
        address = request.form.get("address")
        for i in address_json:
            if i['address'] == address:
                address_json.remove(i)
                db.execute("UPDATE address SET address = ?;", json.dumps(address_json))
                flash(f"Address has been deleted")
                return redirect("/account")
    else:
        return redirect("/account")


@app.route("/orders", methods=["GET", "POST"])
@login_required
def confirm_orders():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    order_details = db.execute("SELECT * FROM orders WHERE user_id = ?", user_id)
    if request.method == "POST":
        cart = db.execute("SELECT cart_items FROM carts WHERE user_id = ?;", user_id)
        if cart:
            cart = cart[0]['cart_items']
        else:
            cart = '[]'
        cart = json.loads( cart )
        address = request.form.get('address_selected')
        order_amount = request.form.get("order_amount")
        for i in cart:
            prod = db.execute("SELECT * FROM products WHERE product_id = ?;", i["product_id"])
            i["product_name"] = prod[0]["product_name"]
            i["price"] = prod[0]["price"]
            i["image"] = prod[0]["image"]
            i["desc"] = prod[0]["desc"]
            i["amount"] = int(prod[0]["price"]) * int(i["qty"])
                
        date_time = datetime.datetime.now()
        order_items = json.dumps(cart)
        # add order details to order table
        db.execute("INSERT INTO orders (user_id, datetime, order_items, order_amount, address, order_status) VALUES(?,?,?,?,?,?)",user_id, date_time, order_items, order_amount, address, 'SUCCESS')
        # empty current cart
        db.execute("UPDATE carts SET cart_items = ?;", '[]')
        # Log transaction
        transaction_amount = -float(order_amount)
        db.execute("INSERT INTO transactions (user_id, tran_type, amount, datetime, tran_status) VALUES(?,?,?,?,?);", user_id, "ORDER_PAYMENT", transaction_amount, datetime.datetime.now(), "SUCCESS")
        # debit order amount from account fund
        db.execute("UPDATE users SET cash = cash - ? WHERE user_id = ?", order_amount, user_id)
        user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
        order_details = db.execute("SELECT * FROM orders WHERE user_id = ?", user_id)
        flash("Order has been placed successfully")
        return render_template("orders.html", user_data=user_data, order_details=order_details)
    return render_template("orders.html", user_data=user_data, order_details=order_details)


@app.route("/view_order", methods=["GET", "POST"])
@login_required
def view_orders():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    order_details = db.execute("SELECT * FROM orders WHERE order_id = ?", request.form.get('order_id'))
    order_items = order_details[0]['order_items']
    order_items = json.loads( order_items )
    return render_template("order_details.html", user_data=user_data, order_details=order_details, order_items=order_items)


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    # get address data of the user
    address = db.execute("SELECT address FROM address WHERE user_id= ?", f'{user_id}')
    address = address[0]['address']
    address = json.loads(address)
    return render_template("account.html", user_data=user_data, address=address)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    cart = db.execute("SELECT cart_items FROM carts WHERE user_id = ?;", user_id)
    if cart:
        cart = cart[0]['cart_items']
    else:
        cart = '[]'
    cart = json.loads( cart )
    sort_by = ''
    sort_direction = [{'reverse':False}]
    if request.method=="POST":
        if request.form.get("search"):
            keyword = request.form.get("search").lower()
            keyword = '%'+keyword+'%'
            word = keyword.replace('%','')
            product_data = db.execute(f"SELECT * FROM products WHERE lower(product_name) LIKE '{keyword}';")
            flash(f"Showing search results for: {word}")
        else:
            return error("Please enter valid search input")            
    
        return render_template("index.html", user_data = user_data, product_data=product_data, cart=cart, sort_by=sort_by, sort_direction=sort_direction)
    return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # get user data
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    # if user has placed a change password request
    if request.method == "POST":
        user_id = session["user_id"]
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if password == confirmation:
            # if not password_strength(password):
            #     return error("password needs to be atleast 6 character, with min 1 upper, 1 lower, 1 digit and 1 special ('@', '#', '_') character", 403)
            hash = generate_password_hash(request.form.get("password"))
            db.execute(f"UPDATE users SET hash = ? WHERE user_id = ?", hash, user_id)
            flash("Your password has been changed successfully")
            return redirect("/")
        else:
            error = "Password Mismatch"
            return render_template("change_password.html", error=error, user_data=user_data)
    # if user is just visiting change password
    return render_template("change_password.html", user_data=user_data)


@app.route("/transactions")
@login_required
def transctions():
    """Show history of transactions"""
    # get user data
    user_id = session["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?;", user_id)
    # get all transaction details of the user
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    # derive date and time data from datetime in transactions
    for i in transactions:
        i["date"] = datetime.datetime.strptime(i["datetime"], '%Y-%m-%d %H:%M:%S').date()
        i["time"] = datetime.datetime.strptime(i["datetime"], '%Y-%m-%d %H:%M:%S').time()
    return render_template("transactions.html", transactions=transactions, user_data=user_data)