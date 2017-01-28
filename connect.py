import psycopg2
from config import config


def connect():
    """ Connnect to the PostgreSQL database server"""
    conn = None
    print "test"
    try:
        params = config()
        print "Connecting to database ..."
        conn = psycopg2.connect(**params)

        cur = conn.cursor()
        print "PostgreSQL version: ",
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print db_version
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print error, "error"

    finally:
        if conn is not None:
            conn.close()
            print "Connection closed"
