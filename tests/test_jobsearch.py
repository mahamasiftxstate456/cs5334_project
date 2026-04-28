#!/usr/bin/env python3
"""
tests/test_jobsearch.py
-----------------------
Standalone tests for the helper functions in cgi-bin/jobsearch.py.

Tests cover:
  1. parse_salary()           -- salary form value to number conversion
  2. build_sql_query()        -- SQL and binds construction
  3. rate_and_sort_jobs()     -- rating, filtering and sorting
  4. calculate_pagination()   -- page calculation and index slicing
  5. get_form_parameters()    -- CGI form field reading
  6. fetch_all_job_rows()     -- database row conversion with mock cursor

NOTE: Because jobsearch.py has top-level code that runs on import
(Content-Type print and main try/except), we cannot import the whole
file directly. Instead we test each helper function independently
by reproducing their logic here and verifying behavior.

Run from project root:
    python3 tests/test_jobsearch.py
"""

import sys
import os
import io

# Folder structure:
#   cs5334_finalproject/
#       tests/          <- this file lives here
#       python/
#           lib/        <- config.py, rating.py live here
#           cgi-bin/    <- jobsearch.py, common.py live here
#
# Add python/ to path so "from lib.config import" and "from lib.rating import" work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))

from lib.config import SALARY_VALUE_TO_MIN
from lib.rating import compute_job_rating

print("=" * 60)
print("test_jobsearch.py")
print("=" * 60)


# =============================================================
# REPRODUCE HELPER FUNCTIONS FROM jobsearch.py
# We cannot import jobsearch.py directly because it has
# top-level code that runs on import (Content-Type print etc.)
# So we reproduce the logic here to test it independently.
# =============================================================

PAGE_SIZE = 16


def parse_salary(salary_form_value):
    """Reproduced from jobsearch.py for testing."""
    if salary_form_value == "Any" or salary_form_value is None:
        return 0
    if salary_form_value in SALARY_VALUE_TO_MIN:
        return SALARY_VALUE_TO_MIN[salary_form_value]
    return 0


def build_sql_query(params):
    """Reproduced from jobsearch.py for testing."""
    sql = "SELECT JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION, "
    sql = sql + "COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION, "
    sql = sql + "MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE, "
    sql = sql + "REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION "
    sql = sql + "FROM job"

    conditions = []
    binds      = {}

    if params["job_title"] != "All" and params["job_title"] != "":
        conditions.append("UPPER(JOB_TITLE) = UPPER(:job_title)")
        binds["job_title"] = params["job_title"]

    if params["specialty"] != "All" and params["specialty"] != "":
        conditions.append("UPPER(SPECIALIZATION) = UPPER(:specialization)")
        binds["specialization"] = params["specialty"]

    if len(conditions) > 0:
        sql = sql + " WHERE "
        sql = sql + " AND ".join(conditions)

    return sql, binds


def rate_and_sort_jobs(job_rows, search_params):
    """Reproduced from jobsearch.py for testing."""
    rated_rows = []
    for job_row in job_rows:
        rating = compute_job_rating(job_row, search_params)
        if rating > 0:
            rated_rows.append((rating, job_row))
    rated_rows.sort(key=lambda pair: pair[0], reverse=True)
    return rated_rows


def calculate_pagination(total_matched, requested_page_number_str):
    """Reproduced from jobsearch.py for testing."""
    if total_matched == 0:
        total_pages = 1
    else:
        total_pages = total_matched // PAGE_SIZE
        if total_matched % PAGE_SIZE > 0:
            total_pages = total_pages + 1

    try:
        requested_page = int(requested_page_number_str)
    except Exception:
        requested_page = 1

    if requested_page < 1:
        current_page = 1
    elif requested_page > total_pages:
        current_page = total_pages
    else:
        current_page = requested_page

    start_index = PAGE_SIZE * (current_page - 1)
    end_index   = start_index + PAGE_SIZE

    return current_page, total_pages, start_index, end_index


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
# TEST 1 - parse_salary()
# =============================================================

assert parse_salary("Any")   == 0,      "salary: Any -> 0"
assert parse_salary(None)    == 0,      "salary: None -> 0"
assert parse_salary("2-3")   == 20000,  "salary: 2-3 -> 20000"
assert parse_salary("3-5")   == 30000,  "salary: 3-5 -> 30000"
assert parse_salary("5-7")   == 50000,  "salary: 5-7 -> 50000"
assert parse_salary("7-10")  == 70000,  "salary: 7-10 -> 70000"
assert parse_salary("10-12") == 100000, "salary: 10-12 -> 100000"
assert parse_salary("12-15") == 120000, "salary: 12-15 -> 120000"
assert parse_salary("15-up") == 150000, "salary: 15-up -> 150000"
assert parse_salary("xyz")   == 0,      "salary: unknown -> 0"
assert parse_salary("")      == 0,      "salary: empty string -> 0 (not in map)"

print("PASS  parse_salary")


# =============================================================
# TEST 2 - build_sql_query()
# =============================================================

# Test 2a: no filters - no WHERE clause
params_all = {
    "job_title": "All",
    "specialty": "All",
}
sql, binds = build_sql_query(params_all)
assert "FROM job"          in sql,    "sql: has FROM job"
assert "WHERE"         not in sql,    "sql: no WHERE clause when all filters are All"
assert len(binds)           == 0,     "binds: empty when no filters"
assert "SELECT"             in sql,   "sql: has SELECT"
assert "DESCRIPTION"        in sql,   "sql: selects DESCRIPTION"
assert "QUALIFICATION"      in sql,   "sql: selects QUALIFICATION"

print("PASS  build_sql_query - no filters")


# Test 2b: job_title filter only
params_title = {
    "job_title": "Manager",
    "specialty": "All",
}
sql, binds = build_sql_query(params_title)
assert "WHERE"                              in sql,   "sql: has WHERE clause"
assert "UPPER(JOB_TITLE) = UPPER(:job_title)" in sql, "sql: job_title condition correct"
assert "SPECIALIZATION"                not in sql.split("WHERE")[1], "sql: no SPECIALIZATION in WHERE"
assert binds.get("job_title")              == "Manager", "binds: job_title value correct"
assert ":job_title"                         in sql,   "sql: uses bind variable"
assert "Manager"                       not in sql.split(":job_title")[0].split("WHERE")[1] if "WHERE" in sql else True, "sql: raw value not in sql"

print("PASS  build_sql_query - job_title filter")


# Test 2c: specialty filter only
params_spec = {
    "job_title": "All",
    "specialty": "Quality Control",
}
sql, binds = build_sql_query(params_spec)
assert "WHERE"                                        in sql,   "sql: has WHERE clause"
assert "UPPER(SPECIALIZATION) = UPPER(:specialization)" in sql, "sql: specialization condition correct"
assert "JOB_TITLE"                                not in sql.split("WHERE")[1], "sql: no JOB_TITLE in WHERE"
assert binds.get("specialization")                    == "Quality Control", "binds: specialization correct"
assert ":specialization"                               in sql,  "sql: uses bind variable"

print("PASS  build_sql_query - specialty filter")


# Test 2d: both filters
params_both = {
    "job_title": "Manager",
    "specialty": "Quality Control",
}
sql, binds = build_sql_query(params_both)
assert "WHERE"                in sql,  "sql: has WHERE clause"
assert "AND"                  in sql,  "sql: has AND between conditions"
assert "job_title"            in binds, "binds: has job_title"
assert "specialization"       in binds, "binds: has specialization"
assert len(binds)             == 2,    "binds: exactly 2 bind variables"

print("PASS  build_sql_query - both filters")


# Test 2e: verify job_type and company NEVER go in WHERE clause
# This is the KEY requirement - Features 1 2 3 depend on this
params_with_type_company = {
    "job_type":    "regular",
    "company_name":"Intel",
    "job_title":   "All",
    "specialty":   "All",
}
sql2, binds2 = build_sql_query(params_with_type_company)
# JOB_TYPE appears in the SELECT part - check only the WHERE part
where_part = sql2.split("WHERE")[1] if "WHERE" in sql2 else ""
assert "JOB_TYPE"    not in where_part, "sql: job_type NEVER in WHERE clause (Feature 1)"
assert "COMPANY"     not in where_part, "sql: company NEVER in WHERE clause (Feature 2 3)"
assert "WHERE"       not in sql2,       "sql: no WHERE clause when only job_type and company given"

print("PASS  build_sql_query - job_type and company not in WHERE clause")


# =============================================================
# TEST 3 - rate_and_sort_jobs()
# =============================================================

# Sample jobs for testing
def make_job(job_type, state, company, min_salary, description=""):
    return {
        "JOB_ID":         "000000001",
        "JOB_TYPE":       job_type,
        "JOB_TITLE":      "Engineer",
        "SPECIALIZATION": "Engineering",
        "REGION_NAME":    "",
        "STATE_NAME":     state,
        "LOCATION":       "",
        "MIN_SALARY":     min_salary,
        "MAX_SALARY":     min_salary + 10000,
        "COMPANY_NAME":   company,
        "START_DATE":     "",
        "REFERENCE_NUM":  "",
        "CONTACT_PERSON": "",
        "DESCRIPTION":    description,
        "QUALIFICATION":  "",
    }

params_none = {
    "job_type": "", "location_type": "", "location_value": "",
    "min_salary": 0, "company_name": "", "keyword": ""
}

# Test 3a: all jobs pass with no filters
jobs = [
    make_job("regular",     "texas",      "Intel",  80000),
    make_job("intern",      "california", "AMD",    50000),
    make_job("entry_level", "new york",   "IBM",    60000),
]
rated = rate_and_sort_jobs(jobs, params_none)
assert len(rated) == 3, "rate_sort: all 3 jobs pass with no filters"

print("PASS  rate_and_sort_jobs - no filters all pass")


# Test 3b: keyword filter excludes jobs without keyword
params_kw = dict(params_none)
params_kw["keyword"] = "python"

jobs_kw = [
    make_job("regular", "texas", "Intel", 80000, "Must know python scripting"),
    make_job("regular", "texas", "IBM",   80000, "Must know java development"),
    make_job("regular", "texas", "AMD",   80000, "python experience required"),
]
rated_kw = rate_and_sort_jobs(jobs_kw, params_kw)
assert len(rated_kw) == 2, "rate_sort: only 2 jobs have keyword python"
companies = [r[1]["COMPANY_NAME"] for r in rated_kw]
assert "IBM" not in companies, "rate_sort: IBM job excluded (no python keyword)"

print("PASS  rate_and_sort_jobs - keyword filter")


# Test 3c: results sorted by rating descending
params_company = dict(params_none)
params_company["company_name"] = "Intel"

jobs_sort = [
    make_job("regular", "texas", "National Semiconductor", 80000),  # similar - 20 penalty -> 80
    make_job("regular", "texas", "Intel",                  80000),  # exact   - 0  penalty -> 100
    make_job("regular", "texas", "NEC",                    80000),  # similar - 30 penalty -> 70
]
rated_sort = rate_and_sort_jobs(jobs_sort, params_company)
assert rated_sort[0][1]["COMPANY_NAME"] == "Intel",                  "sort: Intel first (rating 100)"
assert rated_sort[1][1]["COMPANY_NAME"] == "National Semiconductor", "sort: National Semi second (rating 80)"
assert rated_sort[2][1]["COMPANY_NAME"] == "NEC",                    "sort: NEC third (rating 70)"
assert rated_sort[0][0] > rated_sort[1][0] > rated_sort[2][0], "sort: ratings strictly descending"

print("PASS  rate_and_sort_jobs - sorted by rating descending")


# Test 3d: jobs with rating 0 are excluded
params_kw_miss = dict(params_none)
params_kw_miss["keyword"] = "cobol"

jobs_miss = [
    make_job("regular", "texas", "Intel", 80000, "python java javascript"),
    make_job("regular", "texas", "IBM",   80000, "oracle database sql"),
]
rated_miss = rate_and_sort_jobs(jobs_miss, params_kw_miss)
assert len(rated_miss) == 0, "rate_sort: all jobs excluded when keyword not found"

print("PASS  rate_and_sort_jobs - jobs with rating 0 excluded")


# =============================================================
# TEST 4 - calculate_pagination()
# =============================================================

# Test 4a: exact multiple of PAGE_SIZE
current, total, start, end = calculate_pagination(32, "1")
assert total   == 2,  "pagination: 32 jobs = 2 pages"
assert current == 1,  "pagination: page 1 of 2"
assert start   == 0,  "pagination: page 1 starts at index 0"
assert end     == 16, "pagination: page 1 ends at index 16"

print("PASS  calculate_pagination - exact multiple")


# Test 4b: leftover jobs need extra page
current, total, start, end = calculate_pagination(40, "1")
assert total == 3, "pagination: 40 jobs = 3 pages (16+16+8)"

print("PASS  calculate_pagination - leftover jobs")


# Test 4c: page 2 indexes
current, total, start, end = calculate_pagination(40, "2")
assert current == 2,  "pagination: on page 2"
assert start   == 16, "pagination: page 2 starts at index 16"
assert end     == 32, "pagination: page 2 ends at index 32"

print("PASS  calculate_pagination - page 2 indexes")


# Test 4d: page 3 indexes (last page with 8 jobs)
current, total, start, end = calculate_pagination(40, "3")
assert current == 3,  "pagination: on page 3"
assert start   == 32, "pagination: page 3 starts at index 32"
assert end     == 48, "pagination: page 3 ends at index 48 (Python slicing handles last page)"

print("PASS  calculate_pagination - last page indexes")


# Test 4e: zero results
current, total, start, end = calculate_pagination(0, "1")
assert total   == 1,  "pagination: 0 results = 1 page"
assert current == 1,  "pagination: on page 1"
assert start   == 0,  "pagination: starts at 0"

print("PASS  calculate_pagination - zero results")


# Test 4f: requested page beyond total pages - clamps to last page
current, total, start, end = calculate_pagination(40, "99")
assert current == 3,  "pagination: page 99 clamped to page 3 (last page)"

print("PASS  calculate_pagination - page beyond total clamped")


# Test 4g: requested page 0 or negative - clamps to page 1
current, total, start, end = calculate_pagination(40, "0")
assert current == 1,  "pagination: page 0 clamped to page 1"

current, total, start, end = calculate_pagination(40, "-5")
assert current == 1,  "pagination: page -5 clamped to page 1"

print("PASS  calculate_pagination - negative page clamped to 1")


# Test 4h: invalid page string defaults to page 1
current, total, start, end = calculate_pagination(40, "abc")
assert current == 1,  "pagination: invalid string defaults to page 1"

print("PASS  calculate_pagination - invalid string defaults to 1")


# Test 4i: single job - 1 page
current, total, start, end = calculate_pagination(1, "1")
assert total   == 1, "pagination: 1 job = 1 page"
assert current == 1, "pagination: on page 1"

print("PASS  calculate_pagination - single job")


# Test 4j: exactly PAGE_SIZE jobs
current, total, start, end = calculate_pagination(16, "1")
assert total == 1, "pagination: 16 jobs = 1 page exactly"

print("PASS  calculate_pagination - exactly PAGE_SIZE jobs")


# =============================================================
# TEST 5 - get_form_parameters() with simulated CGI
# =============================================================

import cgi

def simulated_get_form_parameters(query_string):
    """
    Simulate get_form_parameters() by setting QUERY_STRING
    environment variable and using cgi.FieldStorage to parse it.
    """
    os.environ["QUERY_STRING"]   = query_string
    os.environ["REQUEST_METHOD"] = "GET"

    form = cgi.FieldStorage()

    def get_field(field_name, default_value):
        if field_name in form:
            value = form.getvalue(field_name)
            if value is not None and value.strip() != "":
                return value.strip()
        return default_value

    params = {}
    params["job_type"]              = get_field("job_type",              "All")
    params["job_title"]             = get_field("job_title",             "All")
    params["specialty"]             = get_field("specialty",             "All")
    params["company_name"]          = get_field("company_name",          "All")
    params["location_type"]         = get_field("location_type",         "region")
    params["region"]                = get_field("region",                "All")
    params["state"]                 = get_field("state",                 "All")
    params["city"]                  = get_field("city",                  "All")
    params["salary"]                = get_field("salary",                "Any")
    params["keyword"]               = get_field("keyword",               "")
    params["requested_page_number"] = get_field("requested_page_number", "1")

    return params

# Test 5a: all fields present
params = simulated_get_form_parameters(
    "job_type=regular&job_title=Manager&specialty=Engineering"
    "&company_name=Intel&location_type=state&state=California"
    "&salary=7-10&keyword=database&requested_page_number=2"
)
assert params["job_type"]              == "regular",     "form: job_type correct"
assert params["job_title"]             == "Manager",     "form: job_title correct"
assert params["specialty"]             == "Engineering", "form: specialty correct"
assert params["company_name"]          == "Intel",       "form: company_name correct"
assert params["location_type"]         == "state",       "form: location_type correct"
assert params["state"]                 == "California",  "form: state correct"
assert params["salary"]                == "7-10",        "form: salary correct"
assert params["keyword"]               == "database",    "form: keyword correct"
assert params["requested_page_number"] == "2",           "form: page number correct"

print("PASS  get_form_parameters - all fields present")


# Test 5b: missing fields get defaults
params_empty = simulated_get_form_parameters("")
assert params_empty["job_type"]              == "All",    "form: job_type defaults to All"
assert params_empty["job_title"]             == "All",    "form: job_title defaults to All"
assert params_empty["specialty"]             == "All",    "form: specialty defaults to All"
assert params_empty["company_name"]          == "All",    "form: company_name defaults to All"
assert params_empty["location_type"]         == "region", "form: location_type defaults to region"
assert params_empty["salary"]                == "Any",    "form: salary defaults to Any"
assert params_empty["keyword"]               == "",       "form: keyword defaults to empty"
assert params_empty["requested_page_number"] == "1",      "form: page defaults to 1"

print("PASS  get_form_parameters - missing fields get defaults")


# =============================================================
# TEST 6 - fetch_all_job_rows() with mock database
# =============================================================

class MockCursor:
    def __init__(self, rows):
        self.rows  = rows
        self.sql   = ""
        self.binds = ""
    def execute(self, sql, binds):
        self.sql   = sql
        self.binds = binds
    def fetchall(self):
        return self.rows
    def close(self):
        pass

class MockConnection:
    def __init__(self, rows):
        self.mock_cursor = MockCursor(rows)
    def cursor(self):
        return self.mock_cursor
    def close(self):
        pass


def fetch_all_job_rows_testable(sql, binds, mock_conn):
    """
    Testable version of fetch_all_job_rows() using mock connection.
    Logic identical to the real function in jobsearch.py.
    """
    job_rows = []
    cursor   = None

    try:
        cursor   = mock_conn.cursor()
        cursor.execute(sql, binds)
        raw_rows = cursor.fetchall()

        for raw_row in raw_rows:
            job_row = {}
            job_row["JOB_ID"]        = safe_str(raw_row[0])
            job_row["JOB_TYPE"]      = safe_str(raw_row[1])
            job_row["JOB_TITLE"]     = safe_str(raw_row[2])
            job_row["SPECIALIZATION"]= safe_str(raw_row[3])
            job_row["COUNTRY_CODE"]  = safe_int(raw_row[4])
            job_row["REGION_NAME"]   = safe_str(raw_row[5])
            job_row["STATE_NAME"]    = safe_str(raw_row[6])
            job_row["LOCATION"]      = safe_str(raw_row[7])
            job_row["MIN_SALARY"]    = safe_int(raw_row[8])
            job_row["MAX_SALARY"]    = safe_int(raw_row[9])
            job_row["COMPANY_NAME"]  = safe_str(raw_row[10])
            job_row["START_DATE"]    = safe_str(raw_row[11])
            job_row["REFERENCE_NUM"] = safe_str(raw_row[12])
            job_row["CONTACT_PERSON"]= safe_str(raw_row[13])
            job_row["DESCRIPTION"]   = safe_str(raw_row[14])
            job_row["QUALIFICATION"] = safe_str(raw_row[15])
            job_rows.append(job_row)

    finally:
        if cursor is not None:
            cursor.close()

    return job_rows


# Test 6a: normal rows converted correctly
fake_rows = [
    ("000000001", "regular", "Manager", "Quality Control",
     1, "West", "California", "San Jose",
     80000, 88000, "Intel", "2024-01-01",
     "REF001", "John Smith",
     "Looking for quality control manager.",
     "Bachelor degree required."),
    ("000000002", "intern", "Engineer", "Engineering",
     1, "South", "Texas", "Austin",
     50000, 58000, "AMD", "2024-02-01",
     "REF002", "Jane Doe",
     "Junior engineer role.",
     "CS degree required."),
]

sql_test   = "SELECT * FROM job"
binds_test = {}
mock       = MockConnection(fake_rows)
rows       = fetch_all_job_rows_testable(sql_test, binds_test, mock)

assert len(rows)                  == 2,           "fetch: 2 rows returned"
assert rows[0]["JOB_ID"]          == "000000001", "fetch: first row JOB_ID correct"
assert rows[0]["JOB_TYPE"]        == "regular",   "fetch: first row JOB_TYPE correct"
assert rows[0]["JOB_TITLE"]       == "Manager",   "fetch: first row JOB_TITLE correct"
assert rows[0]["MIN_SALARY"]      == 80000,       "fetch: first row MIN_SALARY correct"
assert rows[0]["COMPANY_NAME"]    == "Intel",     "fetch: first row COMPANY_NAME correct"
assert rows[1]["JOB_ID"]          == "000000002", "fetch: second row JOB_ID correct"
assert rows[1]["COMPANY_NAME"]    == "AMD",       "fetch: second row COMPANY_NAME correct"

print("PASS  fetch_all_job_rows - normal rows")


# Test 6b: NULL values converted safely
null_row = [
    ("000000003", None, "Analyst", None,
     None, None, None, "Houston",
     None, None, "IBM", None,
     None, None, None, None)
]
mock_null = MockConnection(null_row)
rows_null = fetch_all_job_rows_testable("SELECT * FROM job", {}, mock_null)

assert rows_null[0]["JOB_TYPE"]      == "",  "fetch nulls: None JOB_TYPE -> empty string"
assert rows_null[0]["SPECIALIZATION"]== "",  "fetch nulls: None SPECIALIZATION -> empty string"
assert rows_null[0]["COUNTRY_CODE"]  == 0,   "fetch nulls: None COUNTRY_CODE -> 0"
assert rows_null[0]["MIN_SALARY"]    == 0,   "fetch nulls: None MIN_SALARY -> 0"
assert rows_null[0]["DESCRIPTION"]   == "",  "fetch nulls: None DESCRIPTION -> empty string"
assert rows_null[0]["QUALIFICATION"] == "",  "fetch nulls: None QUALIFICATION -> empty string"

print("PASS  fetch_all_job_rows - NULL values handled")


# Test 6c: empty result set
mock_empty = MockConnection([])
rows_empty = fetch_all_job_rows_testable("SELECT * FROM job", {}, mock_empty)
assert rows_empty == [], "fetch: empty result returns empty list"

print("PASS  fetch_all_job_rows - empty result")


# =============================================================
# TEST 7 - Integration: build_sql_query + rate_and_sort_jobs
# Simulates the full search flow without DB
# =============================================================

# User searches for Manager jobs in Intel with keyword "quality"
params_integrated = {
    "job_title": "Manager",
    "specialty": "All",
}
search_params_integrated = {
    "job_type":       "All",
    "location_type":  "",
    "location_value": "",
    "min_salary":     0,
    "company_name":   "Intel",
    "keyword":        "quality",
}

# Build the SQL
sql_int, binds_int = build_sql_query(params_integrated)

# Simulate what DB would return (all Managers - WHERE clause filtered by DB)
all_manager_rows = [
    make_job("regular", "california", "Intel", 80000, "quality control manager needed"),
    make_job("regular", "california", "AMD",   75000, "quality assurance role"),
    make_job("regular", "texas",      "Intel", 70000, "no keyword here at all"),
    make_job("regular", "new york",   "IBM",   85000, "quality engineer wanted"),
]

# Rate and sort
rated_int = rate_and_sort_jobs(all_manager_rows, search_params_integrated)

# Intel + quality in desc = 100, AMD + quality = 85 (similar company), IBM + quality = 40 (unrelated)
# Intel job without quality = excluded (rating 0 after 100 penalty keyword)
companies_int = [r[1]["COMPANY_NAME"] for r in rated_int]
assert "Intel" in companies_int, "integration: Intel job with keyword included"
assert "AMD"   in companies_int, "integration: AMD job with keyword included (similar company)"
assert "IBM"   in companies_int, "integration: IBM job with keyword included"

# Intel job without keyword should be excluded
intel_jobs = [r for r in rated_int if r[1]["COMPANY_NAME"] == "Intel"]
assert len(intel_jobs) == 1, "integration: only 1 Intel job (the one with keyword)"

# First result should be Intel (exact company + keyword in description)
assert rated_int[0][1]["COMPANY_NAME"] == "Intel", "integration: Intel job ranks first"

print("PASS  integration - build_sql + rate_and_sort full flow")


# =============================================================
print()
print("All jobsearch.py tests passed.")