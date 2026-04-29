#!/usr/bin/env python3
"""
cgi-bin/jobsearch.py
--------------------
The main job search CGI script. This is the core of the application.
Ported from the demo's jobsearch.pl and ematch_job.pc combined.

What this file does (in order):
  1. Parse CGI form parameters from the GET request
  2. Convert salary form value to a number
  3. Build a SQL query (job_title and specialization in WHERE clause only)
  4. Fetch ALL matching rows from the Oracle database
  5. Rate each row using compute_job_rating() from lib/rating.py
  6. Skip any row whose rating drops to 0 or below
  7. Sort all rated rows by rating (highest first)
  8. Paginate the results (16 per page, same as demo)
  9. Print the HTML results table (same format as demo)
  10. Print pagination links (Next / Previous / Goto page)

KEY DIFFERENCE from the demo:
  In the original demo (ematch_job.pc), job_type and company_name
  were added to the SQL WHERE clause (exact match only).
  In our Python version, these are removed from the WHERE clause
  and handled entirely through the rating system (Features 1, 2, 3).
  Location (region/state/city) was already handled through rating
  in the demo, and we keep it the same way.
  Keyword search (Feature 4) is new - also handled through rating.

Folder: cgi-bin/jobsearch.py

How to access:
  Called automatically when user submits the search form at:
  http://newfirebird.cs.txstate.edu/~netid/html/job_search.html
"""

import sys
import os
import cgi
import cgitb

# Enable CGI error reporting so errors show in browser during development
cgitb.enable()

# Add the project root to Python path so we can import from lib/
# CGI scripts run from cgi-bin/ so we go one level up to find lib/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Add the cgi-bin folder itself to path so we can import common.py
# common.py is in the same folder as this file
# We use os.path.dirname(__file__) which gives us the cgi-bin folder path
# This avoids the "from cgi-bin.common import" syntax error
# because Python cannot import from folders with a dash in the name
sys.path.insert(0, os.path.dirname(__file__))

import cx_Oracle
from lib.db import get_connection
from lib.config import SALARY_VALUE_TO_MIN
from lib.rating import compute_job_rating
from common import print_header
from common import print_footer


# -----------------------------------------------
# PAGE SIZE
# How many results to show per page
# Matches the demo's $page_size = 16
# -----------------------------------------------
PAGE_SIZE = 16


# -----------------------------------------------
# STEP 1: PARSE CGI FORM PARAMETERS
# -----------------------------------------------

def get_form_parameters():
    """
    Read all form parameters from the GET request.
    Equivalent to get_parameters() in the demo's common.cgi.

    The HTML form sends these fields:
        job_type      -- e.g. "regular" or "All"
        job_title     -- e.g. "Manager" or "All"
        specialty     -- e.g. "Quality Control" or "All"
                         (note: form field name is "specialty" but
                          DB column is "specialization")
        company_name  -- e.g. "Intel" or "All"
        location_type -- "region", "state", or "city"
        region        -- e.g. "West" (only used if location_type=region)
        state         -- e.g. "California" (only if location_type=state)
        city          -- e.g. "San Jose" (only if location_type=city)
        salary        -- e.g. "7-10" meaning $70k-$100k, or "Any"
        keyword       -- e.g. "database" (Feature 4, new)
        requested_page_number -- which page of results to show

    Returns:
        A dictionary with all parameter values as strings.
        Missing parameters default to safe empty/All values.
    """

    form = cgi.FieldStorage()

    # Helper function to safely read a form field
    # Returns default_value if the field is missing or empty
    def get_field(field_name, default_value):
        if field_name in form:
            value = form.getvalue(field_name)
            if value is not None and value.strip() != "":
                return value.strip()
        return default_value

    params = {}

    # Job search fields
    params["job_type"]     = get_field("job_type",     "All")
    params["job_title"]    = get_field("job_title",    "All")
    params["specialty"]    = get_field("specialty",    "All")
    params["company_name"] = get_field("company_name", "All")

    # Location fields
    params["location_type"] = get_field("location_type", "region")

    # Read the value for whichever location type was selected
    # Only one of these will be used, determined by location_type
    params["region"] = get_field("region", "All")
    params["state"]  = get_field("state",  "All")
    params["city"]   = get_field("city",   "All")

    # Salary field
    params["salary"] = get_field("salary", "Any")

    # Keyword field (Feature 4 - new, was not in demo backend)
    params["keyword"] = get_field("keyword", "")

    # Pagination - which page to show
    params["requested_page_number"] = get_field("requested_page_number", "1")

    return params


# -----------------------------------------------
# STEP 2: CONVERT SALARY TO A NUMBER
# -----------------------------------------------

def parse_salary(salary_form_value):
    """
    Convert the salary form value to an actual minimum salary number.

    The demo's jobsearch.pl does this with:
        @s2 = split(/-/, $salary);
        $s1 = $s2[0] . "0000";

    We use SALARY_VALUE_TO_MIN from config.py which has the same values.

    Examples:
        "Any"   ->  0       (no salary filter)
        "2-3"   ->  20000   ($20k minimum)
        "7-10"  ->  70000   ($70k minimum)
        "15-up" ->  150000  ($150k minimum)

    Parameters:
        salary_form_value -- the value sent by the salary dropdown

    Returns:
        An integer minimum salary number, or 0 for "Any"
    """

    if salary_form_value == "Any" or salary_form_value is None:
        return 0

    if salary_form_value in SALARY_VALUE_TO_MIN:
        return SALARY_VALUE_TO_MIN[salary_form_value]

    # If value not recognized, return 0 (no salary filter)
    return 0


# -----------------------------------------------
# STEP 3: BUILD THE SQL QUERY
# -----------------------------------------------

def build_sql_query(params):
    """
    Build the SQL SELECT query from the form parameters.

    Ported from prepare_a_job_search_query() in ematch_job.pc,
    but modified for our Python version:

    GOES IN WHERE CLAUSE (exact match):
        - job_title      (same as demo)
        - specialization (same as demo)

    DOES NOT GO IN WHERE CLAUSE (handled by rating instead):
        - job_type      -> Feature 1: rating system
        - company_name  -> Feature 2 & 3: rating system
        - region/state/city -> same as demo (location rating)
        - salary        -> handled by compute_salary_rating()
        - keyword       -> Feature 4: searched in rating

    The demo's ematch_job.pc also had job_type and company_name
    in the WHERE clause. We remove them so ALL jobs are returned
    and then rated, which is what Features 1 and 2 require.

    Parameters:
        params -- the form parameters dictionary from get_form_parameters()

    Returns:
        sql   -- the SQL query string with :placeholders for bind variables
        binds -- a dictionary of bind variable values
    """

    # Start with base query - select all columns
    # The demo uses SELECT * FROM job in ematch_job.pc
    sql = "SELECT JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION, "
    sql = sql + "COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION, "
    sql = sql + "MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE, "
    sql = sql + "REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION "
    sql = sql + "FROM job"

    # Build WHERE clause conditions
    conditions = []
    binds      = {}

    # job_title goes in WHERE clause if not "All"
    # Same as demo's ematch_job.pc
    if params["job_title"] != "All" and params["job_title"] != "":
        conditions.append("UPPER(JOB_TITLE) = UPPER(:job_title)")
        binds["job_title"] = params["job_title"]

    # specialization goes in WHERE clause if not "All"
    # Form field is "specialty" but DB column is "SPECIALIZATION"
    # Same as demo's ematch_job.pc
    if params["specialty"] != "All" and params["specialty"] != "":
        conditions.append("UPPER(SPECIALIZATION) = UPPER(:specialization)")
        binds["specialization"] = params["specialty"]

    # Add WHERE clause only if there are conditions
    if len(conditions) > 0:
        sql = sql + " WHERE "
        sql = sql + " AND ".join(conditions)

    return sql, binds


# -----------------------------------------------
# STEP 4: FETCH ALL ROWS FROM DATABASE
# -----------------------------------------------

def fetch_all_job_rows(sql, binds):
    """
    Execute the SQL query and fetch all matching rows from the database.

    Each row is returned as a dictionary with column names as keys.
    This makes it easy to pass rows to compute_job_rating().

    None values from the DB (NULL columns) are converted to
    empty strings so rating functions can safely call .lower() etc.

    Parameters:
        sql   -- the SQL query string
        binds -- dictionary of bind variable values

    Returns:
        A list of job row dictionaries.
        Returns an empty list if DB query fails.
    """

    job_rows = []
    conn     = None
    cursor   = None

    try:
        conn   = get_connection()
        cursor = conn.cursor()

        # Execute with bind variables to prevent SQL injection
        cursor.execute(sql, binds)

        # Fetch all rows at once
        raw_rows = cursor.fetchall()

        # Convert each row tuple to a named dictionary
        for raw_row in raw_rows:

            # Handle None (NULL) values - convert to empty string
            # so rating functions can safely process them
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

            job_row = {}

            job_row["JOB_ID"]         = safe_str(raw_row[0])
            job_row["JOB_TYPE"]        = safe_str(raw_row[1])
            job_row["JOB_TITLE"]       = safe_str(raw_row[2])
            job_row["SPECIALIZATION"]  = safe_str(raw_row[3])
            job_row["COUNTRY_CODE"]    = safe_int(raw_row[4])
            job_row["REGION_NAME"]     = safe_str(raw_row[5])
            job_row["STATE_NAME"]      = safe_str(raw_row[6])
            job_row["LOCATION"]        = safe_str(raw_row[7])
            job_row["MIN_SALARY"]      = safe_int(raw_row[8])
            job_row["MAX_SALARY"]      = safe_int(raw_row[9])
            job_row["COMPANY_NAME"]    = safe_str(raw_row[10])
            job_row["START_DATE"]      = safe_str(raw_row[11])
            job_row["REFERENCE_NUM"]   = safe_str(raw_row[12])
            job_row["CONTACT_PERSON"]  = safe_str(raw_row[13])
            job_row["DESCRIPTION"]     = safe_str(raw_row[14])
            job_row["QUALIFICATION"]   = safe_str(raw_row[15])

            job_rows.append(job_row)

    except cx_Oracle.DatabaseError as db_error:
        # Return empty list - the caller will show "0 matches"
        job_rows = []

    except Exception as general_error:
        job_rows = []

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

    return job_rows


# -----------------------------------------------
# STEP 5 & 6: RATE AND SORT ALL ROWS
# -----------------------------------------------

def rate_and_sort_jobs(job_rows, search_params):
    """
    Rate every job row using compute_job_rating() and sort by rating.

    Ported from retrieve_matched_job_rows() in ematch_job.pc and
    sort_result_rows() in ematch_class.cxx.

    Logic:
        - Call compute_job_rating() for each row
        - If rating > 0: keep the row with its rating
        - If rating <= 0: discard the row (same as demo)
        - Sort all kept rows from highest rating to lowest

    Parameters:
        job_rows      -- list of job row dictionaries from the database
        search_params -- dictionary passed to compute_job_rating()
            {
                "job_type":       str,
                "location_type":  str,
                "location_value": str,
                "min_salary":     int,
                "company_name":   str,
                "keyword":        str,
            }

    Returns:
        A list of (rating, job_row) tuples sorted by rating descending.
        Only rows with rating > 0 are included.
    """

    rated_rows = []

    for job_row in job_rows:

        # Compute the rating for this job row
        rating = compute_job_rating(job_row, search_params)

        # Only keep jobs with a positive rating
        # Same as demo's: if (temp_rating > 0) insert_a_matched_row(...)
        if rating > 0:
            rated_rows.append((rating, job_row))

    # Sort by rating descending (highest first)
    # Same as demo's sort_result_rows() which sorts in descending order
    rated_rows.sort(key=lambda pair: pair[0], reverse=True)

    return rated_rows


# -----------------------------------------------
# STEP 7: CALCULATE PAGINATION
# -----------------------------------------------

def calculate_pagination(total_matched, requested_page_number_str):
    """
    Calculate pagination values from total results and requested page.

    Ported from the pagination logic in jobsearch.pl.

    The demo uses page_size = 16 and calculates:
        total_page = int(total_matched / page_size)
        if total_page < actual_page: total_page++

    Parameters:
        total_matched             -- total number of matched rows
        requested_page_number_str -- page number as string from form

    Returns:
        current_page -- the actual current page number (1-based)
        total_pages  -- total number of pages
        start_index  -- 0-based index of first result on this page
        end_index    -- 0-based index (exclusive) of last result on this page
    """

    # Calculate total pages - same formula as the demo
    if total_matched == 0:
        total_pages = 1
    else:
        total_pages = total_matched // PAGE_SIZE
        if total_matched % PAGE_SIZE > 0:
            total_pages = total_pages + 1

    # Parse the requested page number
    try:
        requested_page = int(requested_page_number_str)
    except Exception:
        requested_page = 1

    # Validate and clamp the page number
    # Same logic as demo's if/elsif/else block
    if requested_page < 1:
        current_page = 1
    elif requested_page > total_pages:
        current_page = total_pages
    else:
        current_page = requested_page

    # Calculate start and end indexes for slicing the rated_rows list
    # Demo uses: start_entry = page_size * (current_page_number - 1) + 1
    # We use 0-based indexing
    start_index = PAGE_SIZE * (current_page - 1)
    end_index   = start_index + PAGE_SIZE

    return current_page, total_pages, start_index, end_index


# -----------------------------------------------
# STEP 8: PRINT THE RESULTS TABLE
# -----------------------------------------------

def print_results_table(rated_rows, start_index, end_index, total_matched, query_string):
    """
    Print the HTML results table showing one page of results.

    Matches the demo's print_job() function in jobsearch.pl and the
    print_result_rows() function in ematch_class.cxx.

    Table columns (same as demo):
        - Job Number
        - Rating
        - Job Title   (clickable link)
        - Special field (specialization)
        - Location    (city)
        - Company
        - Salary Range

    Row color is #FFFFCC - same as demo.

    Parameters:
        rated_rows    -- sorted list of (rating, job_row) tuples
        start_index   -- 0-based start index for this page
        end_index     -- 0-based end index for this page
        total_matched -- total number of matched rows across all pages
        query_string  -- the original GET query string for pagination links
    """

    print("<center>")
    print("<h2>Job search results</h2>")
    print("(Total " + str(total_matched) + " matches)")
    print("</center>")

    print("<center>")
    print("<table border=1>")

    # Table header - same column names as demo
    print("<tr>")
    print("    <th>Job Number</th>")
    print("    <th>Rating</th>")
    print("    <th>Job Title</th>")
    print("    <th>Special field</th>")
    print("    <th>Location</th>")
    print("    <th>Company</th>")
    print("    <th>Salary Range</th>")
    print("</tr>")

    # Print the rows for the current page
    # Rows are sliced from start_index to end_index
    page_rows = rated_rows[start_index:end_index]

    # Job number displayed to user starts at 1 from the beginning of ALL results
    # not just this page - same as the demo
    job_number = start_index + 1

    for rating, job_row in page_rows:

        # Build the salary range display string
        # Demo shows: result_array[k][8] + "-" + result_array[k][9]
        min_salary = job_row["MIN_SALARY"]
        max_salary = job_row["MAX_SALARY"]

        if min_salary == 0 and max_salary == 0:
            salary_display = "Not specified"
        else:
            salary_display = str(min_salary) + " - " + str(max_salary)

        # Build the job title link - points to getjob.py
        job_id         = job_row["JOB_ID"]
        job_title      = job_row["JOB_TITLE"]
        specialization = job_row["SPECIALIZATION"]
        location       = job_row["LOCATION"]
        company        = job_row["COMPANY_NAME"]

        job_link = "/~netid/cgi-bin/getjob.py"
        job_link = job_link + "?id="        + job_id
        job_link = job_link + "&job_title=" + job_title
        job_link = job_link + "&specialty=" + specialization
        job_link = job_link + "&location="  + location
        job_link = job_link + "&company="   + company
        job_link = job_link + "&salary="    + str(min_salary) + "-" + str(max_salary)

        # Print the row - yellow background #FFFFCC same as demo
        print('<tr bgcolor="#FFFFCC">')
        print("    <td>" + str(job_number) + "</td>")
        print("    <td>" + str(rating) + "</td>")
        print('    <td><a href="' + job_link + '">' + job_title + "</a></td>")
        print("    <td>" + specialization + "</td>")
        print("    <td>" + location + "</td>")
        print("    <td>" + company + "</td>")
        print("    <td>" + salary_display + "</td>")
        print("</tr>")

        job_number = job_number + 1

    print("</table>")
    print("</center>")


# -----------------------------------------------
# STEP 9: PRINT PAGINATION LINKS
# -----------------------------------------------

def print_pagination_links(current_page, total_pages, query_string):
    """
    Print the Next Page, Previous Page, and Goto page links.

    Ported from the pagination link printing in jobsearch.pl.

    The links re-submit the same search with a different
    requested_page_number parameter added to the query string.

    Parameters:
        current_page -- the currently displayed page number
        total_pages  -- total number of pages of results
        query_string -- the original GET query string from the form
    """

    # Remove any existing requested_page_number from query_string
    # so we do not end up with duplicates like:
    # ?...&requested_page_number=5&requested_page_number=6
    params_list        = query_string.split("&")
    cleaned            = []
    for param in params_list:
        if not param.startswith("requested_page_number"):
              cleaned.append(param)
    clean_query_string = "&".join(cleaned)

    base_url = "/~netid/cgi-bin/jobsearch.py?" + clean_query_string

    print("<br>")
    print("(Page " + str(current_page) + " of " + str(total_pages) + ")")
    print("<br>")

    # Next page link
    if current_page < total_pages:
        next_page = current_page + 1
        next_url  = base_url + "&requested_page_number=" + str(next_page)
        print('<a href="' + next_url + '">Next Page &gt;</a>')
    else:
        print("Next Page &gt;")

    print("<br>")

    # Previous page link
    if current_page > 1:
        prev_page = current_page - 1
        prev_url  = base_url + "&requested_page_number=" + str(prev_page)
        print('<a href="' + prev_url + '">&lt; Previous Page</a>')
    else:
        print("&lt; Previous Page")

    print("<br>")

    # Goto page links - only shown if more than 1 page
    # Same as demo's for loop printing individual page numbers
    if total_pages > 1:
        print("Goto page: ")

        page_number = 1
        while page_number <= total_pages:

            if page_number == current_page:
                # Current page shown as plain text (not a link)
                print(str(page_number) + " ")
            else:
                # Other pages shown as links
                page_url = base_url + "&requested_page_number=" + str(page_number)
                print('<a href="' + page_url + '">' + str(page_number) + "</a> ")

            page_number = page_number + 1

    print("<br>")


# -----------------------------------------------
# STEP 10: PRINT ERROR PAGE
# -----------------------------------------------

def print_error_page(error_message):
    """
    Print a simple error page if something goes wrong.
    This prevents the user from seeing a raw Python traceback.

    NOTE: Content-Type is already printed in the main entry point
    before the try block. print_header() here only prints HTML tags.

    Parameters:
        error_message -- string describing what went wrong
    """
    # print_header() handles <html><head><body> opening tags only
    # Content-Type was already printed before the try block
    print_header("Job Search Error")
    print("<center>")
    print("<h2>Job search results</h2>")
    print("<p><b>An error occurred during the search.</b></p>")
    print("<p>" + error_message + "</p>")
    print('<p><a href="/~netid/html/job_search.html">Go back to search</a></p>')
    print("</center>")
    # print_footer() handles </body></html> closing tags
    print_footer()


# ===============================================
# MAIN ENTRY POINT
# This runs when the web server calls jobsearch.py
# ===============================================

# HTTP Content-Type header - printed ONCE here before the try block
# print_header() in common.py does NOT print Content-Type anymore
# so there is no risk of printing it twice
print("Content-Type: text/html")
print()

try:

    # --------------------------------------------------
    # STEP 1: Parse CGI parameters from the form
    # --------------------------------------------------
    params = get_form_parameters()

    # --------------------------------------------------
    # STEP 2: Convert salary form value to a number
    # --------------------------------------------------
    min_salary_number = parse_salary(params["salary"])

    # --------------------------------------------------
    # Figure out which location value the user selected
    # The location_type radio button tells us which
    # dropdown (region/state/city) to read
    # --------------------------------------------------
    location_type = params["location_type"]

    if location_type == "region":
        location_value = params["region"]
    elif location_type == "state":
        location_value = params["state"]
    elif location_type == "city":
        location_value = params["city"]
    else:
        location_type  = "region"
        location_value = "All"

    # --------------------------------------------------
    # Build search_params dict for compute_job_rating()
    # --------------------------------------------------
    search_params = {}
    search_params["job_type"]       = params["job_type"]
    search_params["location_type"]  = location_type
    search_params["location_value"] = location_value
    search_params["min_salary"]     = min_salary_number
    search_params["company_name"]   = params["company_name"]
    search_params["keyword"]        = params["keyword"]

    # --------------------------------------------------
    # STEP 3: Build SQL query
    # Only job_title and specialization go in WHERE clause
    # --------------------------------------------------
    sql, binds = build_sql_query(params)

    # --------------------------------------------------
    # STEP 4: Fetch all rows from the database
    # --------------------------------------------------
    job_rows = fetch_all_job_rows(sql, binds)

    # --------------------------------------------------
    # STEP 5 & 6: Rate each row and sort by rating
    # --------------------------------------------------
    rated_rows    = rate_and_sort_jobs(job_rows, search_params)
    total_matched = len(rated_rows)

    # --------------------------------------------------
    # STEP 7: Calculate pagination
    # --------------------------------------------------
    current_page, total_pages, start_index, end_index = calculate_pagination(
        total_matched,
        params["requested_page_number"]
    )

    # --------------------------------------------------
    # Get the original query string for pagination links
    # --------------------------------------------------
    query_string = os.environ.get("QUERY_STRING", "")

    # --------------------------------------------------
    # Print the HTML page
    # print_header() only prints HTML tags - not Content-Type
    # Content-Type was already printed above before try block
    # --------------------------------------------------
    print_header("Job Search Results")

    # --------------------------------------------------
    # STEP 8: Print the results table
    # --------------------------------------------------
    print_results_table(
        rated_rows,
        start_index,
        end_index,
        total_matched,
        query_string
    )

    # --------------------------------------------------
    # STEP 9: Print pagination links
    # --------------------------------------------------
    print_pagination_links(current_page, total_pages, query_string)

    print_footer()

except Exception as top_level_error:
    # Content-Type already printed before try block - do not print again
    # print_error_page calls print_header which only prints HTML tags now
    print_error_page(str(top_level_error))