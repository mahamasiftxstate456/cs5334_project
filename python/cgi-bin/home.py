#!/usr/bin/env python3
"""
cgi-bin/home.py
---------------
The homepage for the job search application.
Ported from the demo's home.pl.

What this file does:
  1. Connects to the Oracle database
  2. Counts total rows in job, member, and c_g tables
     (same three counts as the demo's real_time_number binary)
  3. Prints an HTML page showing those counts
     with the same UI as the professor's demo

The demo used a compiled C binary (real_time_number) to get
the counts. In our Python version we query the DB directly
using cx_Oracle, which is simpler and cleaner.

Folder: cgi-bin/home.py

How to run:
    Accessed via web browser at:
    http://newfirebird.cs.txstate.edu/~netid/cgi-bin/home.py
"""

import sys
import os

# Add the project root to Python path so we can import from lib/
# This is needed because CGI scripts run from the cgi-bin folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import cx_Oracle
from lib.db import get_connection


def get_table_counts():
    """
    Connect to the Oracle database and count rows in
    the job, member, and c_g tables.

    This replaces the demo's real_time_number binary which
    did the same three SELECT COUNT(*) queries in Pro*C.

    Returns:
        job_count    -- total number of jobs in the job table
        member_count -- total number of members in the member table
        cg_count     -- total number of college graduates in the c_g table

    If any query fails, that count is returned as 0.
    """

    job_count    = 0
    member_count = 0
    cg_count     = 0

    conn   = None
    cursor = None

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # Count total jobs - same as demo's cursor c1
        cursor.execute("SELECT COUNT(*) FROM job")
        result = cursor.fetchone()
        if result is not None:
            job_count = result[0]

        # Count total members (Registered Engineers) - same as demo's cursor c2
        cursor.execute("SELECT COUNT(*) FROM member")
        result = cursor.fetchone()
        if result is not None:
            member_count = result[0]

        # Count college graduates - same as demo's cursor c3
        cursor.execute("SELECT COUNT(*) FROM c_g")
        result = cursor.fetchone()
        if result is not None:
            cg_count = result[0]

    except cx_Oracle.DatabaseError as db_error:
        # If DB fails, we still show the page with 0 counts
        # rather than crashing the whole page
        job_count    = 0
        member_count = 0
        cg_count     = 0

    except Exception as general_error:
        job_count    = 0
        member_count = 0
        cg_count     = 0

    finally:
        # Always close cursor and connection cleanly
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

    return job_count, member_count, cg_count


def print_home_page(job_count, member_count, cg_count):
    """
    Print the complete HTML homepage.
    Matches the professor's demo home.pl output exactly:
      - Cyan background (#00FFFF) - note: different from other pages
      - Welcome title
      - Live counts from database
      - Tagline text (exact wording from demo)
      - Navigation links
      - Copyright line

    Parameters:
        job_count    -- total jobs from database
        member_count -- total members from database
        cg_count     -- total college graduates from database
    """

    # ----------------------------------------
    # HTTP Content-Type header
    # MUST be printed first before any HTML
    # ----------------------------------------
    print("Content-Type: text/html")
    print()

    # ----------------------------------------
    # HTML opening tags
    # Background is CYAN (#00FFFF) - same as demo
    # This is different from the results page (#FFFFFF)
    # ----------------------------------------
    print("<html>")
    print("<head>")
    print("<title>DrPengsAIIPDemos Job Search</title>")
    print('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">')
    print("</head>")
    print('<body BGCOLOR="#00FFFF" LINK="#0088ff" ALINK="#FF0000" VLINK="#CC0000">')

    # ----------------------------------------
    # Welcome title - exact wording from demo
    # ----------------------------------------
    print("<center><h2>DrPengsAIIPDemos Welcomes You!</h2></center>")
    print("<center>")
    print("<br>")
    print("<br>")

    # ----------------------------------------
    # Live database counts
    # Same three numbers as demo's real_time_number binary:
    #   array[1] = member count  -> Registered Engineers
    #   array[0] = job count     -> Total jobs
    #   array[2] = c_g count     -> Total registered college graduates
    # ----------------------------------------
    print("<center>")
    print("<i>")
    print("Registered Engineers: " + str(member_count) + "<br>")
    print("Total jobs: " + str(job_count) + "<br>")
    print("Total registered college graduates: " + str(cg_count) + "<br>")
    print("</i>")
    print("</center>")
    print("<br>")
    print("<br>")

    # ----------------------------------------
    # Tagline - exact wording from demo
    # ----------------------------------------
    print("<b>")
    print("DrPengsAIIPDemos.com will assist and challenge you to be")
    print("where you can be in the 21th centry in the high tech,")
    print("high competitive, high reward world.")
    print("</b>")
    print("<br>")
    print("<br>")
    print("<br>")

    # ----------------------------------------
    # Navigation links
    # Updated from .pl to .py
    # Matches demo's table-based nav layout
    # ----------------------------------------
    print('<table cellspacing="0" cellpadding="3" border="0">')
    print("<tr>")
    print('    <td><a href="/~netid/cgi-bin/home.py">Home</a>')
    print('    <td><a href="/~netid/html/job_search.html">Job Search</a>')
    print('    <td><a href="/~netid/demo/proc/unix-version/html/employer_login.html">Employers</a>')
    print('    <td><a href="/~netid/demo/proc/unix-version/html/member_login.html">Members</a>')
    print("</tr>")
    print("</table>")
    print("</center>")

    # ----------------------------------------
    # Copyright line - exact wording from demo
    # ----------------------------------------
    print("<br>")
    print("<i>Copyright &copy;2023 DrPengsAIIPDemos.com Inc. All rights reserved.</i>")

    # ----------------------------------------
    # HTML closing tags
    # ----------------------------------------
    print("</body>")
    print("</html>")


def print_error_page(error_message):
    """
    Print a simple error page if something goes critically wrong
    before we even get to the database query.

    Parameters:
        error_message -- string describing what went wrong
    """

    print("Content-Type: text/html")
    print()
    print("<html>")
    print("<head><title>Error</title></head>")
    print('<body BGCOLOR="#00FFFF">')
    print("<center><h2>DrPengsAIIPDemos Welcomes You!</h2></center>")
    print("<center>")
    print("<p><b>Error loading page:</b> " + error_message + "</p>")
    print('<p><a href="/~netid/html/job_search.html">Go to Job Search</a></p>')
    print("</center>")
    print("</body>")
    print("</html>")


# -----------------------------------------------
# MAIN ENTRY POINT
# This runs when the web server calls home.py
# -----------------------------------------------
try:
    # Step 1: Get counts from the database
    job_count, member_count, cg_count = get_table_counts()

    # Step 2: Print the complete homepage
    print_home_page(job_count, member_count, cg_count)

except Exception as error:
    # If anything goes wrong at the top level,
    # print an error page instead of a blank screen
    print_error_page(str(error))