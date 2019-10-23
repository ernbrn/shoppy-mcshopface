import sqlite3
import json

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def seed_groceries(db):
    with current_app.open_resource('inventory.json') as json_file:
        groceries = json.loads(json_file.read())['data']
        for grocery in groceries:
            db.execute(
                'INSERT INTO groceries (name, brand, price, quantity) VALUES (?, ?, ?, ?)',
                (
                    grocery['name'],
                    grocery['brand'],
                    grocery['price'],
                    grocery['quantity']
                )
            )
            db.commit()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    seed_groceries(db)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
