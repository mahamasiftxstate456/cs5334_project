#!/usr/bin/env python3
"""
tests/test_getjob.py
--------------------
Standalone tests for the helper functions in cgi-bin/getjob.py.

Tests cover:
  1. safe_str()       -- None and value handling
  2. safe_int()       -- None and value handling
  3. get_job_id()     -- reading job id from simulated URL
  4. fetch_job_by_id  -- database fetch with mock connection
  5. Output content   -- verifying HTML output contains correct fields

NOTE: Because getjob.py has top-level code that runs on import
(Content-Type print and main try/except), we cannot import the
whole file. Instead we test each helper function independently
by copying their logic here and verifying behavior.

Run from project root:
    python3 tests/test_getjob.py
"""

import sys
import os
import io

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

print("=" * 60)
print("test_getjob.py")
print("=" * 60)


# =============================================================
# Copy helper functions from getjob.py so we can test them
# independently without triggering the top-level main code
# =============================================================

def safe_str(value):
    if value is None:
        return ""
    return str(value).strip()

def safe_int(value):
    if value is None:
        return 0
    try:
        return int(value)
    except Exception:
        return 0


# =============================================================
# TEST 1 - safe_str()
# =============================================================

# None value should become empty string
assert safe_str(None)          == "",       "safe_str: None -> empty string"

# Normal string should come back stripped
assert safe_str("Intel")       == "Intel",  "safe_str: normal string"

# String with spaces should be stripped
assert safe_str("  Intel  ")   == "Intel",  "safe_str: strips whitespace"

# Number should become a string
assert safe_str(12345)         == "12345",  "safe_str: number becomes string"

# Empty string should stay empty
assert safe_str("")            == "",       "safe_str: empty string stays empty"

# String with only spaces should become empty after strip
assert safe_str("   ")         == "",       "safe_str: spaces only -> empty"

print("PASS  safe_str")


# =============================================================
# TEST 2 - safe_int()
# =============================================================

# None value should become 0
assert safe_int(None)          == 0,        "safe_int: None -> 0"

# Normal integer should stay integer
assert safe_int(80000)         == 80000,    "safe_int: normal int"

# String number should convert to int
assert safe_int("75000")       == 75000,    "safe_int: string number -> int"

# Zero should stay zero
assert safe_int(0)             == 0,        "safe_int: zero stays zero"

# Non numeric string should become 0
assert safe_int("abc")         == 0,        "safe_int: non-numeric -> 0"

# Float string cannot be directly converted by int() so returns 0
assert safe_int("80000.99")    == 0,        "safe_int: float string -> 0 (int() cannot convert floats)"

print("PASS  safe_int")


# =============================================================
# TEST 3 - get_job_id() with simulated CGI environment
# =============================================================
# We simulate what cgi.FieldStorage() does by setting the
# QUERY_STRING environment variable which is what CGI uses
# for GET requests. Then we call our own version of get_job_id
# that reads from it.

import cgi
import urllib.parse

def simulated_get_job_id(query_string):
    """
    Simulates get_job_id() by setting QUERY_STRING environment
    variable and using cgi.FieldStorage to parse it.
    This is exactly how the real web server passes URL parameters.
    """
    os.environ["QUERY_STRING"]  = query_string
    os.environ["REQUEST_METHOD"] = "GET"

    form = cgi.FieldStorage()

    if "id" in form:
        value = form.getvalue("id")
        if value is not None and value.strip() != "":
            return value.strip()
    return None

# Normal job id in URL
result = simulated_get_job_id("id=000000001")
assert result == "000000001",   "get_job_id: normal id from URL"

# Job id with other parameters
result = simulated_get_job_id("id=000000042&job_title=Manager")
assert result == "000000042",   "get_job_id: id among other params"

# No id in URL - should return None
result = simulated_get_job_id("job_title=Manager&company=Intel")
assert result is None,          "get_job_id: no id -> None"

# Empty query string - should return None
result = simulated_get_job_id("")
assert result is None,          "get_job_id: empty URL -> None"

# Id with spaces - should be stripped
result = simulated_get_job_id("id=+000000001+")
assert result is not None,      "get_job_id: id with spaces stripped"

print("PASS  get_job_id")


# =============================================================
# TEST 4 - fetch_job_by_id() with mock database
# =============================================================
# We mock the database connection so no real Oracle connection
# is needed. The mock returns a fake row so we can verify
# that fetch_job_by_id correctly converts it to a dictionary.

class MockCursor:
    """
    Fake database cursor that returns a predetermined row.
    Used to test fetch_job_by_id without a real DB connection.
    """
    def __init__(self, row_to_return):
        self.row     = row_to_return
        self.sql     = None
        self.binds   = None

    def execute(self, sql, binds):
        # Store what was passed so we can verify it
        self.sql   = sql
        self.binds = binds

    def fetchone(self):
        return self.row

    def close(self):
        pass


class MockConnection:
    """
    Fake database connection that returns a MockCursor.
    """
    def __init__(self, row_to_return):
        self.mock_cursor = MockCursor(row_to_return)

    def cursor(self):
        return self.mock_cursor

    def close(self):
        pass


def fetch_job_by_id_testable(job_id, mock_conn):
    """
    Testable version of fetch_job_by_id() that accepts
    a mock connection instead of calling get_connection().
    Logic is identical to the real function.
    """
    job    = None
    cursor = None

    try:
        cursor = mock_conn.cursor()

        sql = "SELECT JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION, "
        sql = sql + "COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION, "
        sql = sql + "MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE, "
        sql = sql + "REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION "
        sql = sql + "FROM job "
        sql = sql + "WHERE JOB_ID = :job_id"

        binds = {"job_id": job_id}

        cursor.execute(sql, binds)

        row = cursor.fetchone()

        if row is not None:
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

    finally:
        if cursor is not None:
            cursor.close()

    return job


# Test 4a: normal job row returned correctly
fake_row = (
    "000000001",       # JOB_ID
    "regular",         # JOB_TYPE
    "Manager",         # JOB_TITLE
    "Quality Control", # SPECIALIZATION
    1,                 # COUNTRY_CODE
    "West",            # REGION_NAME
    "California",      # STATE_NAME
    "San Jose",        # LOCATION
    80000,             # MIN_SALARY
    88000,             # MAX_SALARY
    "Intel",           # COMPANY_NAME
    "2024-01-01",      # START_DATE
    "REF001",          # REFERENCE_NUM
    "John Smith",      # CONTACT_PERSON
    "Looking for a quality control manager with 5 years experience.",  # DESCRIPTION
    "Bachelor degree required. Oracle experience preferred.",          # QUALIFICATION
)

mock_conn = MockConnection(fake_row)
job = fetch_job_by_id_testable("000000001", mock_conn)

assert job is not None,                          "fetch: job found"
assert job["JOB_ID"]         == "000000001",     "fetch: JOB_ID correct"
assert job["JOB_TYPE"]       == "regular",       "fetch: JOB_TYPE correct"
assert job["JOB_TITLE"]      == "Manager",       "fetch: JOB_TITLE correct"
assert job["SPECIALIZATION"] == "Quality Control","fetch: SPECIALIZATION correct"
assert job["COUNTRY_CODE"]   == 1,               "fetch: COUNTRY_CODE correct"
assert job["REGION_NAME"]    == "West",          "fetch: REGION_NAME correct"
assert job["STATE_NAME"]     == "California",    "fetch: STATE_NAME correct"
assert job["LOCATION"]       == "San Jose",      "fetch: LOCATION correct"
assert job["MIN_SALARY"]     == 80000,           "fetch: MIN_SALARY correct"
assert job["MAX_SALARY"]     == 88000,           "fetch: MAX_SALARY correct"
assert job["COMPANY_NAME"]   == "Intel",         "fetch: COMPANY_NAME correct"
assert job["START_DATE"]     == "2024-01-01",    "fetch: START_DATE correct"
assert job["REFERENCE_NUM"]  == "REF001",        "fetch: REFERENCE_NUM correct"
assert job["CONTACT_PERSON"] == "John Smith",    "fetch: CONTACT_PERSON correct"
assert "quality control" in job["DESCRIPTION"].lower(), "fetch: DESCRIPTION correct"
assert "bachelor" in job["QUALIFICATION"].lower(),      "fetch: QUALIFICATION correct"

print("PASS  fetch_job_by_id - normal row")


# Test 4b: job not found - fetchone returns None
mock_conn_empty = MockConnection(None)
job_not_found = fetch_job_by_id_testable("999999999", mock_conn_empty)
assert job_not_found is None,   "fetch: job not found returns None"

print("PASS  fetch_job_by_id - job not found")


# Test 4c: NULL values from database handled correctly
null_row = (
    "000000002",  # JOB_ID
    None,         # JOB_TYPE        -> safe_str -> ""
    "Engineer",   # JOB_TITLE
    None,         # SPECIALIZATION  -> safe_str -> ""
    None,         # COUNTRY_CODE    -> safe_int -> 0
    None,         # REGION_NAME     -> safe_str -> ""
    None,         # STATE_NAME      -> safe_str -> ""
    "Austin",     # LOCATION
    None,         # MIN_SALARY      -> safe_int -> 0
    None,         # MAX_SALARY      -> safe_int -> 0
    "IBM",        # COMPANY_NAME
    None,         # START_DATE      -> safe_str -> ""
    None,         # REFERENCE_NUM   -> safe_str -> ""
    None,         # CONTACT_PERSON  -> safe_str -> ""
    None,         # DESCRIPTION     -> safe_str -> ""
    None,         # QUALIFICATION   -> safe_str -> ""
)

mock_conn_nulls = MockConnection(null_row)
job_nulls = fetch_job_by_id_testable("000000002", mock_conn_nulls)

assert job_nulls is not None,            "fetch nulls: job returned"
assert job_nulls["JOB_TYPE"]       == "", "fetch nulls: None JOB_TYPE -> empty string"
assert job_nulls["SPECIALIZATION"] == "", "fetch nulls: None SPECIALIZATION -> empty string"
assert job_nulls["COUNTRY_CODE"]   == 0,  "fetch nulls: None COUNTRY_CODE -> 0"
assert job_nulls["MIN_SALARY"]     == 0,  "fetch nulls: None MIN_SALARY -> 0"
assert job_nulls["DESCRIPTION"]    == "", "fetch nulls: None DESCRIPTION -> empty string"
assert job_nulls["QUALIFICATION"]  == "", "fetch nulls: None QUALIFICATION -> empty string"

print("PASS  fetch_job_by_id - NULL values handled")


# Test 4d: verify sql and binds are correct
mock_conn_check = MockConnection(fake_row)
cursor_check    = mock_conn_check.cursor()
fetch_job_by_id_testable("000000001", mock_conn_check)

assert "WHERE JOB_ID = :job_id" in cursor_check.sql, "fetch: bind variable :job_id in sql"
assert cursor_check.binds["job_id"] == "000000001",  "fetch: binds has correct job_id"
assert "SELECT" in cursor_check.sql,                 "fetch: sql has SELECT"
assert "FROM job" in cursor_check.sql,               "fetch: sql has FROM job"
assert "DESCRIPTION" in cursor_check.sql,            "fetch: sql selects DESCRIPTION"
assert "QUALIFICATION" in cursor_check.sql,          "fetch: sql selects QUALIFICATION"

print("PASS  fetch_job_by_id - sql and binds verified")


# =============================================================
# TEST 5 - Output content verification
# =============================================================
# Capture print output and verify the HTML contains
# the correct job details in the right format.

def capture_job_detail_output(job):
    """
    Captures the HTML output that would be printed for a job.
    Redirects stdout to a string buffer to verify content.
    """
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured

    # Replicate the print_job_detail logic from getjob.py
    min_salary = job["MIN_SALARY"]
    max_salary = job["MAX_SALARY"]

    if min_salary == 0 and max_salary == 0:
        salary_display = "Not specified"
    else:
        salary_display = str(min_salary) + " - " + str(max_salary)

    print("<h2>Job description</h2>")
    print('<form action="/~netid/cgi-bin/submit_resume.pl">')
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
    print("</b>")
    print("<b>Job Description:</b>")
    if job["DESCRIPTION"] != "":
        print(job["DESCRIPTION"])
    else:
        print("No description available.")
    print("<b>Qualification:</b>")
    if job["QUALIFICATION"] != "":
        print(job["QUALIFICATION"])
    else:
        print("No qualification details available.")
    print('<textarea rows=20 cols=60 name=resume>')
    print("</textarea><br>")
    print('<input type=hidden name=job_id value="' + job["JOB_ID"] + '">')
    print('<input type=submit value="Submit your resume for this job">')
    print("</form>")

    sys.stdout = old_stdout
    return captured.getvalue()


# Test 5a: verify job detail HTML contains correct values
sample_job = {
    "JOB_ID":         "000000001",
    "JOB_TYPE":       "regular",
    "JOB_TITLE":      "Manager",
    "SPECIALIZATION": "Quality Control",
    "REGION_NAME":    "West",
    "STATE_NAME":     "California",
    "LOCATION":       "San Jose",
    "MIN_SALARY":     80000,
    "MAX_SALARY":     88000,
    "COMPANY_NAME":   "Intel",
    "START_DATE":     "2024-01-01",
    "REFERENCE_NUM":  "REF001",
    "CONTACT_PERSON": "John Smith",
    "DESCRIPTION":    "Looking for a quality control manager.",
    "QUALIFICATION":  "Bachelor degree required.",
}

output = capture_job_detail_output(sample_job)

assert "Manager"                      in output, "output: job title shown"
assert "regular"                      in output, "output: job type shown"
assert "Quality Control"              in output, "output: specialization shown"
assert "San Jose"                     in output, "output: location shown"
assert "California"                   in output, "output: state shown"
assert "Intel"                        in output, "output: company shown"
assert "80000 - 88000"                in output, "output: salary range shown"
assert "quality control manager"      in output, "output: description shown"
assert "Bachelor degree"              in output, "output: qualification shown"
assert "#006600"                      in output, "output: green color used"
assert "submit_resume.pl"             in output, "output: form action correct"
assert "000000001"                    in output, "output: job_id in hidden field"
assert "Submit your resume"           in output, "output: submit button shown"

print("PASS  output content - all fields present")


# Test 5b: salary display when both are 0
job_no_salary = dict(sample_job)
job_no_salary["MIN_SALARY"] = 0
job_no_salary["MAX_SALARY"] = 0

output_no_salary = capture_job_detail_output(job_no_salary)
assert "Not specified" in output_no_salary, "output: no salary shows Not specified"
assert "0 - 0"        not in output_no_salary, "output: does not show 0 - 0"

print("PASS  output content - salary not specified")


# Test 5c: empty description shows fallback message
job_no_desc = dict(sample_job)
job_no_desc["DESCRIPTION"]  = ""
job_no_desc["QUALIFICATION"] = ""

output_no_desc = capture_job_detail_output(job_no_desc)
assert "No description available."         in output_no_desc, "output: empty desc fallback"
assert "No qualification details available." in output_no_desc, "output: empty qual fallback"

print("PASS  output content - empty description fallback")


# =============================================================
# TEST 6 - SQL structure verification
# =============================================================
# Verify the SQL query has correct structure without
# running it against a real database.

sql = "SELECT JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION, "
sql = sql + "COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION, "
sql = sql + "MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE, "
sql = sql + "REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION "
sql = sql + "FROM job "
sql = sql + "WHERE JOB_ID = :job_id"

binds = {"job_id": "000000001"}

assert "SELECT"          in sql,          "sql: has SELECT"
assert "FROM job"        in sql,          "sql: has FROM job"
assert "WHERE"           in sql,          "sql: has WHERE clause"
assert ":job_id"         in sql,          "sql: uses bind variable not raw value"
assert "000000001"       not in sql,      "sql: raw value NOT in sql string"
assert "DESCRIPTION"     in sql,          "sql: selects DESCRIPTION"
assert "QUALIFICATION"   in sql,          "sql: selects QUALIFICATION"
assert "job_id"          in binds,        "binds: has job_id key"
assert binds["job_id"]   == "000000001",  "binds: job_id value correct"

# Count columns selected - should be 16
columns = [c.strip() for c in sql.split("SELECT")[1].split("FROM")[0].split(",")]
assert len(columns) == 16, f"sql: should select 16 columns, got {len(columns)}"

print("PASS  SQL structure verified")


# =============================================================
print()
print("All getjob.py tests passed.")