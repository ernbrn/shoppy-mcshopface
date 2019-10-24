import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mcshopface.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import grocery
    app.register_blueprint(grocery.bp)

    from . import cart
    app.register_blueprint(cart.bp)

    from . import cart_groceries
    app.register_blueprint(cart_groceries.bp)

    from . import purchase
    app.register_blueprint(purchase.bp)

    from . import receipt
    app.register_blueprint(receipt.bp)

    from . import reset
    app.register_blueprint(reset.bp)

    return app
