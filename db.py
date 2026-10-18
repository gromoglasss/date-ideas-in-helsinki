import sqlite3
from flask import g
import config

def get_connection():
    con = sqlite3.connect(config.database_file)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def last_insert_id():
    return g.last_insert_id

def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def execute_file(filename):
    with open(filename, encoding="utf-8") as file:
        sql = file.read()
    con = get_connection()
    con.executescript(sql)
    con.close()

def init_db():
    execute_file("schema.sql")

    # the possible classes are added only once
    class_count = query("SELECT COUNT(id) FROM classes")[0][0]
    if class_count == 0:
        execute_file("init.sql")
