import os
import json
from flask import Flask, render_template, session, request, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from flask_session import Session
from functools import wraps
import datetime
import requests



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


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    orders = db.execute("SELECT * FROM orders;")
    return render_template("client-home.html", orders=orders)


@app.route("/client_order_details", methods=["GET", "POST"])
def client_order_details():
    # get order_id
    order_id = request.form.get("order_id")
    # get order data
    order_details = db.execute("SELECT * FROM orders WHERE order_id = ?", order_id)
    # get user data
    user_id = order_details[0]["user_id"]
    user_data = db.execute("SELECT * FROM users WHERE user_id = ?", user_id)
    order_items = order_details[0]["order_items"]
    order_items = json.loads(order_items)
    return render_template("client_order_details.html", order_items=order_items, order_details=order_details, user_data=user_data)        


@app.route("/status_change", methods=["GET", "POST"])
def status_change():
    order_id = request.form.get("order_id")
    date = datetime.datetime.now()
    date = date.strftime("%d %b %Y %I:%M %p")
    status = "Shipped on " + str(date)
    db.execute("UPDATE orders SET order_status = ? WHERE order_id = ?", status, order_id)
    flash(f"Order status have been updated")
    return redirect("/")