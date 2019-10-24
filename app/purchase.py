from flask import (Blueprint, request)

from app.db import get_db
from app.api_helpers import (
    last_inserted_row, array_of_dicts_from_rows, return_dict)
from app.cart_helpers import get_cart_by_id
from werkzeug.exceptions import abort

bp = Blueprint('purchase', __name__)


@bp.route('/purchase', methods=['POST'])
def purchase():
    json_body = request.get_json()
    cart_id = json_body['cart_id']
    money_sent = json_body['usd_paid']
    db = get_db()

    if not cart_id:
        abort(406, 'Must include cart id')

    cart = get_cart_by_id(cart_id)
    grocery_rows = db.execute(grocery_query(), (cart_id,)).fetchall()

    if not grocery_rows:
        abort(406, 'No groceries exist for cart id')

    ensure_cart_is_unpurchased(cart)

    grocery_list = array_of_dicts_from_rows(grocery_rows)
    ensure_purchase_amount(cart, money_sent)

    for grocery in grocery_list:
        check_stock(grocery)
        adjust_current_inventory(grocery)

    mark_cart_purchased(cart_id)

    return return_dict(create_receipt(cart, money_sent))


def ensure_cart_is_unpurchased(cart):
    if cart['purchased'] == 1:
        abort(406, 'Cart cannot be purchased, it is already purchased')


def ensure_purchase_amount(cart, money_sent):
    if cart['total_price'] > money_sent:
        abort(406, 'Not enough money for purchase')


def check_stock(grocery):
    stocked_quantity = grocery['quantity']
    requested_quantity = grocery['requested_quantity']
    name = grocery['name']

    if stocked_quantity < requested_quantity:
        abort(
            406, "Unacceptable quantity of {0}: {1} requested, {2} in stock".format(name, requested_quantity, stocked_quantity))


def adjust_current_inventory(grocery):
    new_quantity = grocery['quantity'] - grocery['requested_quantity']
    grocery_id = grocery['id']

    db = get_db()
    db.execute('UPDATE groceries SET quantity = ? WHERE id = ?',
               (new_quantity, grocery_id,))


def mark_cart_purchased(cart_id):
    db = get_db()
    db.execute('UPDATE carts SET purchased = 1 WHERE id = ?', (cart_id,))


def create_receipt(cart, paid_amount):
    total_price = cart['total_price']
    change_given = paid_amount - total_price

    db = get_db()
    db.execute(
        'INSERT INTO receipts (cart_id, paid_amount, change_given, total_price) values (?, ?, ?, ?)', (cart['id'], paid_amount, change_given, total_price))
    db.commit()

    return last_inserted_row(db, 'receipts')


def grocery_query():
    return ('SELECT g.*, cg.quantity as requested_quantity FROM carts '
            'INNER JOIN cart_groceries cg ON cg.cart_id = carts.id '
            'INNER JOIN groceries g ON g.id = cg.grocery_id '
            'WHERE carts.id = ?')
