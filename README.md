# Grocery Deli
#### Video Demo:  <URL https://www.youtube.com/watch?v=HZX1rmvlooE>
#### Description: 
Grocery Deli is an e-commerce web and mobile app, that enables any grocery business to let customers place orders and client to fulfill the orders.

There are two apps in this project:
#### **Customer side app**
User stories:
- User can register and login with email ID and password
- Once logged in, user will be able to view entire product catalogue, available funds, and his/her cart
- User will be able to view USPs of the app through carousel banners
- User can use sort and filter function to find products easily 
- User can also search for any product 
- User can decide qty for each items and add them to cart 
- User can go to cart and select an address from the address book
- If address book is empty, user can enter an address for delivery in the address book
- Once address has been added, user can review the cart. User can also delete items from the cart
- User can now go to summary and review the order details, address and payment
- User can add enough funds to the account to place the order
- After placing the order user can view the placed order details and status of the order in the order section
- Once Client has shipped the order, user should be able to see updated order status against the order
- User can also go to account to see his/her personal details
- User should be able to view added addresses, add/delete addresses
- User should be able to see all transactions (i.e. Add fund, Order Placing)
- User should be able to change password and logout
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
flask run
```
To run the client side app: (In new terminal)
```
python -m flask --app client run --host 0.0.0.0 --port 5001
```

#### **Validations implemented** (Frontend + Backend)
- User can't view logged in section without logging in
- User can't enter sql queries in the input fields to temper with the database
- User can't submit empty orders and enter non-integer/ absurd quantities
- User can't enter an empty search
- User can't add non-integer/ absurd inputs to add fund
- User can add empty address
- User shouldn't be able to see other user's data

#### **Design considerations**
The customer app is designed to be mobile first. The app is responsive enough to accommodate Computer/Laptop view as well. The color pallet uses `#54B435` and `#198754` as the primary color.

#### **Languages used**
- Python: Flask app creation, routing, calculations
- HTML: Creating webpages
- Javascript: Dynamic HTML
- JINJA2: Templating HTMLs with data
- CSS and Bootstrap: Adding design elements. [Iconify](https://iconify.design/) have been used for icons
#### **Future Development Roadmap**
- Adding more features to the customer app (i.e. Category pages, better search capability, Payment gateway, Notification system)
- Adding more features in the client app (i.e. Inventory management, P&L Dashboard, Add/ Remove Products, notifications)
- Adding delivery side app for updating status of shipment delivery
- Adding more CSS/ Bootstrap elements to make interactions more engaging
- Building the apps in react.js to make them single page applications 
- Hosting the apps on external servers
#### _disclaimers:_
- The product images and names have been taken from a existing ecommerce app called "BBDaily" in India
- The product prices and discounts are randomly generated
