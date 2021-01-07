import psycopg2
import os
from dotenv import load_dotenv

import click
from flask import current_app, g
from flask.cli import with_appcontext

load_dotenv()

db_name = os.getenv("DEV_DB")


def get_pg_cursor_conn():
    if 'conn' not in g:
        g.conn = psycopg2.connect(dbname=db_name)
    if 'cursor' not in g:
        g.cursor = g.conn.cursor()
        
    return (g.conn, g.cursor)

def close_conn(e=None):
    conn = g.pop('conn')
    cursor = g.pop('cursor')

    if conn is not None:
        conn.close()
    
    if cursor is not None:
        cursor.close()

def init_db():
    conn, cursor = get_pg_cursor_conn()
    with open('app/schema.sql','r') as sql_file:
        cursor.execute(sql_file.read())
        conn.commit()

def init_test_db():
    db_name = os.getenv("TEST_DB")
    g.conn = psycopg2.connect(dbname=db_name)
    g.cursor = g.conn.cursor()
    with open('app/schema.sql','r') as sql_file:
        g.cursor.execute(sql_file.read())
        g.conn.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_conn)
    app.cli.add_command(init_db_command)
