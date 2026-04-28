#!/usr/bin/env python3
"""
cgi-bin/getjob.py
-----------------
The job detail page. Shows full information about a single job.

This is an IMPROVED version of the demo's getjob.pl.

What the demo's getjob.pl did:
  - Read job details from URL parameters only
  - Never queried the database
  - DESCRIPTION was used but never assigned so it was always blank

What our getjob.py does better:
  - Uses the job_id from the URL to query the database
  - Fetches the complete job row including DESCRIPTION and QUALIFICATION
  - Shows all job details properly including the full description
  - Matches the same UI as the demo (green color #006600 for values)

How it is accessed:
  User clicks a job title link in the search results page.
  The link passes job_id in the URL.
  Example URL:
    /~netid/cgi-bin/getjob.py?id=000000001

Folder: cgi-bin/getjob.py
"""

import sys
import os
import cgi
import cgitb

# Enable CGI error reporting so errors show in browser during development
cgitb.enable()

# Add the project root to Python path so we can import from lib/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Add the cgi-bin folder itself to path so we can import common.py
# common.py is in the same folder as this file (cgi-bin/)
# This avoids the "from cgi-bin.common import" syntax error
# because Python cannot import from folders with a dash in the name
sys.path.insert(0, os.path.dirname(__file__))

import cx_Oracle
from lib.db import get_connection
from common import print_header
from common import print_footer


# -----------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------

def safe_str(value):
    """
    Converts None database value to empty string.
    Oracle returns NULL columns as None in Python.
    Calling .strip() or .lower() on None would crash.
    """
    if value is None:
        return ""
    return str(value).strip()


def safe_int(value):
    """
    Converts None database value to 0.
    Oracle returns NULL number columns as None.
    Doing math on None would crash.
    """
    if value is None:
        return 0
    try:
        return int(value)
    except Exception:
        return 0


def get_job_id():
    """
    Read the job id from the URL parameters.
    The job title link passes the job id as ?id=000000001 in the URL.

    Returns:
        job_id -- string job id, or None if not found
    """
    form = cgi.FieldStorage()

    if "id" in form:
        value = form.getvalue("id")
        if value is not None and value.strip() != "":
            return value.strip()

    return None


def fetch_job_by_id(job_id):
    """
    Query the database for the full job row using job_id.

    sql and binds are defined as separate variables before
    cursor.execute() is called. This makes the code clearer -
    you can see exactly what query will run and what values
    will be substituted before execution happens.

    Parameters:
        job_id -- the job id string from the URL

    Returns:
        A dictionary with all job column values.
        Returns None if job not found or query fails.
    """

    conn   = None
    cursor = None
    job    = None

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # sql defined separately - the query with :placeholder
        sql = "SELECT JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION, "
        sql = sql + "COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION, "
        sql = sql + "MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE, "
        sql = sql + "REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION "
        sql = sql + "FROM job "
        sql = sql + "WHERE JOB_ID = :job_id"

        # binds defined separately - maps placeholder to actual value
        # Oracle replaces :job_id with the actual job_id value safely
        # The URL value never goes directly into the SQL string
        # This prevents SQL injection attacks
        binds = {
            "job_id": job_id
        }

        # Execute using both sql and binds as separate variables
        cursor.execute(sql, binds)

        row = cursor.fetchone()

        if row is not None:

            # Build the job dictionary - column order matches SELECT above
            job = {}
            job["JOB_ID"]         = safe_str(row[0])
            job["JOB_TYPE"]       = safe_str(row[1])
            job["JOB_TITLE"]      = safe_str(row[2])
            job["SPECIALIZATION"] = safe_str(row[3])
            job["COUNTRY_CODE"]   = safe_int(row[4])
            job["REGION_NAME"]    = safe_str(row[5])
            job["STATE_NAME"]     = safe_str(row[6])
            job["LOCATION"]       = safe_str(row[7])
            job["MIN_SALARY"]     = safe_int(row[8])
            job["MAX_SALARY"]     = safe_int(row[9])
            job["COMPANY_NAME"]   = safe_str(row[10])
            job["START_DATE"]     = safe_str(row[11])
            job["REFERENCE_NUM"]  = safe_str(row[12])
            job["CONTACT_PERSON"] = safe_str(row[13])
            job["DESCRIPTION"]    = safe_str(row[14])
            job["QUALIFICATION"]  = safe_str(row[15])

    except cx_Oracle.DatabaseError as db_error:
        job = None

    except Exception as general_error:
        job = None

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

    return job


# ===============================================
# MAIN ENTRY POINT
# This runs when the web server calls getjob.py
#
# Content-Type is printed ONCE here at the very top
# before the try block. It is never printed again
# anywhere - not even in the except block.
#
# print_header() in common.py does NOT print Content-Type
# so there is no risk of printing it twice.
#
# All page output is written directly inside the
# try/except blocks. No separate print_not_found,
# print_no_id, or print_error functions needed.
# ===============================================

# Content-Type printed ONCE here - never again
print("Content-Type: text/html")
print()

try:

    # Print page header - only prints HTML tags, not Content-Type
    print_header("Job Description")

    # Read job_id from URL
    job_id = get_job_id()

    # No job id case
    if job_id is None:

        print("<h2>No Job Selected</h2>")
        print("<p>No job ID was provided.</p>")
        print('<p><a href="/~netid/html/job_search.html">Go back to Job Search</a></p>')

    else:

        # Fetch full job row from database using job_id
        job = fetch_job_by_id(job_id)

        # Job not found case
        if job is None:

            print("<h2>Job Not Found</h2>")
            print("<p>Job ID <b>" + str(job_id) + "</b> was not found in the database.</p>")
            print('<p><a href="/~netid/html/job_search.html">Go back to Job Search</a></p>')

        else:

            # Build salary display string
            min_salary = job["MIN_SALARY"]
            max_salary = job["MAX_SALARY"]

            if min_salary == 0 and max_salary == 0:
                salary_display = "Not specified"
            else:
                salary_display = str(min_salary) + " - " + str(max_salary)

            # Page heading - same as demo
            print("<h2>Job description</h2>")

            # Resume form - submit_resume.pl was never provided in demo
            print('<form action="/~netid/cgi-bin/submit_resume.pl">')

            # Job details in green color #006600 - same as demo
            print("<b>")

            print("Job Title:")
            print('<font color="#006600"> ' + job["JOB_TITLE"] + " </font>")
            print("<br>")

            print("Job Type:")
            print('<font color="#006600"> ' + job["JOB_TYPE"] + " </font>")
            print("<br>")

            print("Specialized area:")
            print('<font color="#006600"> ' + job["SPECIALIZATION"] + " </font>")
            print("<br>")

            print("Location:")
            print('<font color="#006600"> ' + job["LOCATION"] + ", " + job["STATE_NAME"] + " </font>")
            print("<br>")

            print("Company:")
            print('<font color="#006600"> ' + job["COMPANY_NAME"] + " </font>")
            print("<br>")

            print("Salary Range:")
            print('<font color="#006600"> ' + salary_display + " </font>")
            print("<br>")

            print("Start Date:")
            print('<font color="#006600"> ' + job["START_DATE"] + " </font>")
            print("<br>")

            print("Contact Person:")
            print('<font color="#006600"> ' + job["CONTACT_PERSON"] + " </font>")
            print("<br>")

            print("Reference Number:")
            print('<font color="#006600"> ' + job["REFERENCE_NUM"] + " </font>")
            print("<br>")

            print("</b>")

            # Job Description - fetched from database
            # IMPROVEMENT over demo - demo never showed this
            print("<br>")
            print("<b>Job Description:</b>")
            print("<br>")

            if job["DESCRIPTION"] != "":
                print(job["DESCRIPTION"])
            else:
                print("No description available.")

            print("<br>")
            print("<br>")

            # Qualification - fetched from database
            # Also not shown in demo's getjob.pl
            print("<b>Qualification:</b>")
            print("<br>")

            if job["QUALIFICATION"] != "":
                print(job["QUALIFICATION"])
            else:
                print("No qualification details available.")

            print("<br>")
            print("<br>")

            # Resume submission area - same as demo
            print("Copy and paste your text resume into the following window")
            print(" if interested.<br>")
            print('<textarea rows=20 cols=60 name=resume>')
            print("</textarea><br>")
            print('<input type=hidden name=job_id value="' + job["JOB_ID"] + '">')
            print('<input type=submit value="Submit your resume for this job">')
            print("</form>")

    # Print page footer - closes </body></html>
    print_footer()


# Content-Type NOT printed here again
except Exception as top_level_error:

    print("<h2>Error</h2>")
    print("<p>" + str(top_level_error) + "</p>")
    print('<p><a href="/~netid/html/job_search.html">Go back to Job Search</a></p>')
    print_footer()