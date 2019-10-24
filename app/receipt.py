from flask import (Blueprint)

from app.db import get_db
from app.api_helpers import return_list

bp = Blueprint('receipt', __name__)


@bp.route('/receipts')
def grocery_routes():
    db = get_db()
    rows = db.execute('SELECT * FROM receipts').fetchall()
    return return_list(rows)
