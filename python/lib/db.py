#!/usr/bin/env python3
"""
lib/db.py
---------
Handles ONE thing only: connecting to the Oracle database.

Any other file that needs the database will import get_connection() from here.
If credentials ever change, you only update this one file.

Usage (from another file):
    from lib.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()
    # ... do your queries ...
    cursor.close()
    conn.close()
"""
import os

# -----------------------------------------------
# Oracle client environment variables
# Must be set BEFORE cx_Oracle is imported so
# the library can locate the Oracle client files
# on newfirebird.cs.txstate.edu
# -----------------------------------------------
os.environ["ORACLE_HOME"]      = "/usr/lib/oracle/21/client64"
os.environ["LD_LIBRARY_PATH"]  = "/usr/lib/oracle/21/client64/lib"
os.environ["TNS_ADMIN"]        = "/usr/lib/oracle/21/client64/network/admin"

import cx_Oracle

# -----------------------------------------------
# YOUR DATABASE CREDENTIALS
# Fill these in once, never touch again
# -----------------------------------------------
DB_USER     = ""           # your txstate username
DB_PASSWORD = ""   # your oracle password
DB_DSN      = "csdbora"         # service name
# -----------------------------------------------


def get_connection():
    """
    Opens and returns a connection to the Oracle database.

    Returns:
        conn -- a cx_Oracle connection object

    Raises:
        cx_Oracle.DatabaseError if connection fails
    """
    conn = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN)
    return conn


# -----------------------------------------------
# This block ONLY runs when you do: python3 db.py
# It is IGNORED when another file imports this file
# -----------------------------------------------
if __name__ == "__main__":
    print("Testing database connection...")
    try:
        conn = get_connection()
        print("SUCCESS - Connected to Oracle!")
        conn.close()
        print("Connection closed cleanly.")

    except cx_Oracle.DatabaseError as e:
        print(f"FAILED - Database error: {e}")
    except Exception as e:
        print(f"FAILED - Unexpected error: {e}")