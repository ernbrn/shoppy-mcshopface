from flask import (Blueprint, request)

from app.db import get_db
from app.api_helpers import (
    return_list, return_dict, last_inserted_row)
from app.cart_helpers import get_cart_by_id

bp = Blueprint('cart', __name__)


@bp.route('/carts', methods=('GET', 'POST'))
def root_routes():
    if request.method == 'GET':
        return index()
    elif request.method == 'POST':
        return create()


@bp.route('/carts/<int:cart_id>')
def show(cart_id):
    return get_cart_by_id(cart_id)


def index():
    db = get_db()
    rows = db.execute('SELECT * FROM carts').fetchall()
    return return_list(rows)


def create():
    db = get_db()
    db.execute('INSERT INTO carts (purchased) values (false)')
    db.commit()

    return return_dict(last_inserted_row(db, 'carts'))
