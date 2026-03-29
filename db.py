import sqlite3
from config import DATABASE

def get_connection():
    return sqlite3.connect(DATABASE)