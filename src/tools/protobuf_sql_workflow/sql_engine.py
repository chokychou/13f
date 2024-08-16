import psycopg2
import os
import sys
from dataclasses import dataclass

@dataclass
class DbConfig:
    host: str
    database: str
    user: str
    password: str
    port: str

class SqlEngine:

    def __init__(self, db_config: DbConfig):
        self.conn = connect_to_db(
            db_config.host, 
            db_config.database,
            db_config.user, 
            db_config.password,
            db_config.port
        )

    def __del__(self):
        close_connection(self.conn)

    def execute_query(self, query, options=()):
        execute_query(self.conn, query, options)


def connect_to_db(host, database, user, password, port):
    """Connects to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None

def execute_query(conn, query, options=()):
    """Executes a SQL query."""
    cursor = conn.cursor()
    cursor.execute(query, options)
    conn.commit()
    cursor.close()


def close_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
        print("PostgreSQL connection is closed")
