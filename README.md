# Grocery Deli
#### Video Demo:  <URL HERE>
#### Description: 
Grocery Deli is an e-commerce web and mobile app, that enables any grocery business to let their user place an order and fulfill the orders.

There are two apps in this project:
#### **Customer side app**
User stories:
- User can register and login with email ID and password
- Once logged in, user will be able to view entire product catalogue, available funds, and his/her cart.
- User will be able to view USPs of the app through carosel banners
- User can use sort and filter function to find products easily. 
- User can also search for any product. 
- User can decide qty for each items and add them to cart. 
Once done adding items to cart, user can go to cart and enter an address for delivery (user to be able to select the same address for future orders). 
- Once address has been added, user can review the cart. User can also delete items from the cart. 
- User can now go to summary and review the order details, address and payment. 
- User can add enough fund to the account to place the order. 
- After placing the order user can view the placed order details and status of the order in the order section. 
- User can also go to account to see his/her personal details
- User should be able to view added addresses, add/delete addresses
- User should be able to see all transactions (i.e. Add fund, Order Placing)
- User should be able to change password and logout.
- User should explained about errors in case of improper usage

#### **Client side app**
User stories:
- User can view all orders placed by customers
- User can view details of any order
- User should be able to update the status of the order from Pending to Shipped with timestamp

#### **Project File structures explained**
- `app.py`: Customer side flask app file
- `client.py`: Client side flask app file
- `ecomm.db`: database storing all data, connecting to both app.py and client.py
- `templates`: includes html pages for both customer app and client app
- `static`: includes images for products, banners and style.css
- `style.css`: main css file
- `flask_session` and `__pycache__` are flask app generated folders

#### **Running the apps:**
To run the customer side app:
```
run flask
```
To run the client side app: (In new terminal)
```
--app client run --host 0.0.0.0 --port 5001
```

#### **Validations implemented**
- User can't view logged in section without logging in
- User can't enter sql queries in the input fields to temper with the database
- User can't submit empty orders and enter non-integer/ absurd quanities
- User can't enter an empty search
- User can't add non-integer/ absurd inputs to add fund
- User can add empty address
- User shouldn't be able to see other user's data
