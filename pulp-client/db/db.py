import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import os

#get_db starts as well as connects to sqlite db(named as pulp) via a socket. Also creates a db named "pulp".
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            "pulp", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# close_db closes a database connection if its already running.
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

# init_db basically creates schema.sql into a table.
# "with current_app.open_resource("db/schema.sql") as f" basically automatically calls f.close after its body's execution.
def init_db():
    db = sqlite3.connect(
            "pulp", detect_types=sqlite3.PARSE_DECLTYPES
        )
    db.row_factory = sqlite3.Row

    with open("db/schema.sql") as f:
        db.executescript(f.read())

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

#teardown closes database
#add_command calls init db which creates and connects to the db.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

if __name__ == '__main__':
    init_db()
