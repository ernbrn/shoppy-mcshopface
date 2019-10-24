# Shoppy McShopface

Welcome to the country's premier luxury online shopping API! Read on for instructions and get ready to shoppy your McFace off.

## Get the app running

1. Make sure you have Python, Flask, and a virtual environment
   setup and running. [Setup instructions here](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask).
2. From the project root run the following:

```
  export FLASK_APP=app
  export FLASK_ENV=development
```

3. Initialize the database:

```
  flask init-db
```

4. Start the server:

```
  flask run
```

5. Check your server output for your server address, and use that for your base url.

## How it works (for those new to grocery shopping)

Take a look at the groceries. When you find some you like, create a cart and add your groceries to your cart. You can take a look at your cart at any time to see what you have in there and what it will all cost. When you're ready to check out, you may purchase the contents of your cart (and receive a receipt). All prices are assumed to be USD and are represented in cents.

## API Documentation

### groceries

**GET /groceries** View all groceries

### carts

**GET /carts** View all shopping carts

**POST /carts** Create a new shopping cart (this endpoint accepts no POST body)

**GET /carts/:id** View your cart, all groceries in your cart, purchase status, and total price of your cart.

### cart_groceries

**POST /cart_groceries** Add a grocery to your cart

```
Example post body (all fields are required):
{
  "cart_id": 2,
  "grocery_id": 5,
  "quantity": 2
}
```

### purchase

**POST /purchase** Purchase a cart of groceries. Return value is a receipt object.

```
Example post body (all fields are required):
{
  "cart_id": 2,
  "usd_paid": 500
}
```

### receipts

**GET /receipts** View all receipts

### Burn it all down

**DELETE /reset** Reset the inventory, reset the logs, remove all carts.
