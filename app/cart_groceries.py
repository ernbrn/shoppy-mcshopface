from flask import (Blueprint, request)

from app.db import get_db
from app.api_helpers import (return_dict, last_inserted_row)
from app.cart_helpers import get_cart_by_id
from werkzeug.exceptions import abort

bp = Blueprint('cart_groceries', __name__)


@bp.route('/cart_groceries', methods=['POST'])
def post_functions():
    json_body = request.get_json()
    cart_id = json_body['cart_id']
    grocery_id = json_body['grocery_id']
    requested_quantity = json_body['quantity']
    db = get_db()

    current_stock_quantity = quantity_in_stock(grocery_id)

    if current_stock_quantity < requested_quantity:
        abort(406, "Unacceptable quantity of {0}, only {1} left in stock".format(
            requested_quantity, current_stock_quantity))

    existing_record = db.execute(
        'SELECT * FROM cart_groceries WHERE cart_id = ? AND grocery_id = ?', (cart_id, grocery_id,)).fetchone()

    if existing_record:
        return update(existing_record, requested_quantity)

    return create(cart_id, grocery_id, requested_quantity)


def update(existing_record, new_quantity):
    db = get_db()
    cart_groceries_id = existing_record['id']
    cart = get_cart_by_id(existing_record['cart_id'])

    if cart['purchased'] == 1:
        abort(406, 'Cannot add groceries to purchaed cart')

    db.execute('UPDATE cart_groceries SET quantity = ? WHERE id = ?',
               (new_quantity, cart_groceries_id))
    db.commit()
    updated_cart_groceries_record = db.execute(
        'SELECT * FROM cart_groceries WHERE id = ?', (cart_groceries_id,)).fetchone()

    return return_dict(updated_cart_groceries_record)


def create(cart_id, grocery_id, quantity):
    db = get_db()
    db.execute(
        'INSERT INTO cart_groceries (cart_id, grocery_id, quantity) values (?, ?, ?)', (cart_id, grocery_id, quantity))
    db.commit()
    return return_dict(last_inserted_row(db, 'cart_groceries'))


def quantity_in_stock(grocery_id):
    db = get_db()
    row = db.execute(
        'SELECT quantity FROM groceries WHERE id = ?', (grocery_id,)).fetchone()
    if row is None:
        return 0

    return row['quantity']
