from flask import (Blueprint)

from app.db import init_db

bp = Blueprint('reset', __name__)


@bp.route('/reset', methods=['DELETE'])
def reset():
    init_db()
    return 'ok'
