from flask import (Blueprint)

from app.db import get_db
from app.api_helpers import return_list

bp = Blueprint('grocery', __name__)


@bp.route('/groceries')
def grocery_routes():
    db = get_db()
    rows = db.execute('SELECT * FROM groceries').fetchall()
    return return_list(rows)
