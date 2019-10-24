from app.api_helpers import array_of_dicts_from_rows
from app.db import get_db


def get_cart_by_id(cart_id):
    db = get_db()
    rows = db.execute(cart_query(), (cart_id,)).fetchall()
    items_in_cart = array_of_dicts_from_rows(rows)
    cart_row = db.execute(cart_purchased_query(),
                          (cart_id,)).fetchone()

    purchased = cart_row['purchased'] if cart_row else 0

    return {
        'id': cart_id,
        'items': items_in_cart,
        'total_price': calculate_cart_price(items_in_cart),
        'purchased': purchased
    }


def cart_query():
    return ('SELECT g.name, g.brand, g.price, cg.quantity FROM carts '
            'INNER JOIN cart_groceries cg ON cg.cart_id = carts.id '
            'INNER JOIN groceries g ON g.id = cg.grocery_id '
            'WHERE carts.id = ?')


def cart_purchased_query():
    return 'SELECT purchased FROM carts WHERE id = ?'


def calculate_cart_price(items):
    total_price = 0
    for item in items:
        total_price += (item['price'] * item['quantity'])

    return total_price
