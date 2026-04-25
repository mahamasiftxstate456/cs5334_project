# =======================================================
# jobsearch.py - IMPLEMENTATION GUIDE
# =======================================================
# This is the MAIN CGI script for the job search project.
# It is called automatically by the web server when the
# user submits the search form at job_search.html.
#
# DEPENDENT FILES:
#   Make sure these are implemented and working first:
#
#   1. lib/db.py
#      - get_connection() : used by fetch_all_job_rows()
#        to connect to Oracle database
#
#   2. lib/config.py
#      - SALARY_VALUE_TO_MIN : used by parse_salary()
#        to convert form salary code to a number
#
#   3. lib/rating.py
#      - compute_job_rating() : used by rate_and_sort_jobs()
#        to rate every job row from the database
#
#   4. lib/location_data.py
#      - find_region_index() : used in compute_job_rating()
#      - find_state_index()  : used in compute_job_rating()
#      - find_city_index()   : used in compute_job_rating()
#
#   5. cgi-bin/common.py
#      - print_header() : used to print HTML page header
#      - print_footer() : used to print HTML page footer
#
#   6. html/job_search.html
#      - The search form that sends data to this script
#      - Form action must point to this file
#
# PAGE_SIZE = 16
#   Show 16 results per page same as the demo
#
# =======================================================
# FUNCTIONS TO IMPLEMENT (in this order)
# =======================================================
#
# -------------------------------------------------------
# 1. get_form_parameters()
# -------------------------------------------------------
# PURPOSE:
#   Read ALL form fields submitted by the user from
#   the HTML search form. Equivalent to get_parameters()
#   in the demo's common.cgi.
#
# HOW TO IMPLEMENT:
#   - Use Python's built in cgi.FieldStorage() to read
#     the GET request from the browser
#   - Write a small helper function get_field(name, default)
#     that safely reads one field and returns default if
#     the field is missing or empty
#   - Read these fields from the form:
#     job_type              -> default "All"
#     job_title             -> default "All"
#     specialty             -> default "All"
#       NOTE: form field is "specialty" but DB column
#             is "SPECIALIZATION" - map this in build_sql_query()
#     company_name          -> default "All"
#     location_type         -> default "region"
#     region                -> default "All"
#     state                 -> default "All"
#     city                  -> default "All"
#     salary                -> default "Any"
#     keyword               -> default "" (empty string)
#     requested_page_number -> default "1"
#   - Return all values in a dictionary called params
#
# RETURNS: dictionary with all form field values as strings
#
# -------------------------------------------------------
# 2. parse_salary(salary_form_value)
# -------------------------------------------------------
# PURPOSE:
#   Convert the salary dropdown form code to an actual
#   minimum salary number for use in rating calculations.
#
# HOW TO IMPLEMENT:
#   - If salary_form_value is "Any" or None return 0
#     (0 means no salary filter applied)
#   - Look up salary_form_value in SALARY_VALUE_TO_MIN
#     dictionary from config.py and return the number
#   - If value not recognized return 0 as safe default
#
# EXAMPLE:
#   "Any"   -> 0
#   "2-3"   -> 20000
#   "7-10"  -> 70000
#   "15-up" -> 150000
#
# RETURNS: integer minimum salary number, 0 means no filter
#
# -------------------------------------------------------
# 3. build_sql_query(params)
# -------------------------------------------------------
# PURPOSE:
#   Build the SQL SELECT query from the form parameters.
#   Ported from prepare_a_job_search_query() in demo's
#   ematch_job.pc but MODIFIED for our Python version.
#
# IMPORTANT - WHAT GOES IN WHERE CLAUSE:
#   ONLY these two fields go in the SQL WHERE clause:
#     - job_title      (exact match, same as demo)
#     - specialization (exact match, same as demo)
#       NOTE: form sends "specialty" but column is "SPECIALIZATION"
#
#   These fields do NOT go in WHERE clause (handled by rating):
#     - job_type     -> Feature 1: rating system
#     - company_name -> Feature 2 and 3: rating system
#     - location     -> location rating functions
#     - salary       -> compute_salary_rating()
#     - keyword      -> compute_keyword_rating()
#
#   REASON: If job_type or company_name go in WHERE clause
#   then only exact matches come back from database and
#   Features 1, 2, 3 cannot work. We need ALL jobs to
#   come back so rating can filter and rank them.
#
# HOW TO IMPLEMENT:
#   - Start with base SQL selecting ALL columns from job table:
#     SELECT JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION,
#     COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION,
#     MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE,
#     REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION
#     FROM job
#   - Create empty list called conditions and empty dict called binds
#   - If job_title != "All" and job_title != "":
#     Add "UPPER(JOB_TITLE) = UPPER(:job_title)" to conditions
#     Add job_title value to binds dict
#   - If specialty != "All" and specialty != "":
#     Add "UPPER(SPECIALIZATION) = UPPER(:specialization)" to conditions
#     Add specialty value to binds dict
#   - If conditions list is not empty add WHERE clause to SQL
#     joining conditions with AND between each one
#   - Return both sql string and binds dictionary
#
# NOTE ON BIND VARIABLES:
#   Use :placeholders in SQL and pass values separately in binds.
#   This prevents SQL injection attacks. Oracle replaces
#   :job_title with the actual value safely.
#
# RETURNS: (sql string, binds dictionary)
#
# -------------------------------------------------------
# 4. fetch_all_job_rows(sql, binds)
# -------------------------------------------------------
# PURPOSE:
#   Execute the SQL query against Oracle database and
#   return all matching rows as a list of dictionaries.
#
# HOW TO IMPLEMENT:
#   - Call get_connection() from lib/db.py to open connection
#   - Create a cursor from the connection
#   - Execute sql with binds using cursor.execute(sql, binds)
#   - Fetch all rows using cursor.fetchall()
#     Each row comes back as a plain tuple with no column names
#   - Write two small helper functions:
#     safe_str(value) -> converts None to "" and strips spaces
#     safe_int(value) -> converts None to 0
#     These are needed because NULL columns from Oracle
#     come back as None in Python and calling .lower() on
#     None would crash the rating functions
#   - Convert each tuple to a named dictionary with these keys:
#     JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION,
#     COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION,
#     MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE,
#     REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION
#     NOTE: column order must match the SELECT order in build_sql_query()
#           position 0 = JOB_ID, position 1 = JOB_TYPE, etc.
#   - Use safe_str() for text columns and safe_int() for number columns
#     Number columns: COUNTRY_CODE (pos 4), MIN_SALARY (pos 8), MAX_SALARY (pos 9)
#   - Append each dictionary to job_rows list
#   - Wrap everything in try/except/finally
#     On any error return empty list so caller shows "0 matches"
#     Always close cursor and connection in finally block
#
# RETURNS: list of job row dictionaries, empty list if DB fails
#
# -------------------------------------------------------
# 5. rate_and_sort_jobs(job_rows, search_params)
# -------------------------------------------------------
# PURPOSE:
#   Rate every job row and sort by rating highest first.
#   Ported from retrieve_matched_job_rows() and
#   sort_result_rows() in demo's ematch_class.cxx
#
# HOW TO IMPLEMENT:
#   - Create empty list called rated_rows
#   - Loop through every job_row in job_rows
#   - For each job_row call compute_job_rating(job_row, search_params)
#     from lib/rating.py - this returns a number 0 to 100
#   - If rating > 0 add (rating, job_row) as a TUPLE to rated_rows
#     If rating is 0 or below discard the job completely
#     Same as demo's: if (temp_rating > 0) insert_a_matched_row()
#   - After loop sort rated_rows by rating descending (highest first)
#     Use: rated_rows.sort(key=lambda pair: pair[0], reverse=True)
#     Same as demo's sort_result_rows()
#   - Return sorted rated_rows list
#
# NOTE ON TUPLE:
#   We store (rating, job_row) as a tuple not a list because:
#   - Tuple communicates these two things belong together permanently
#   - Tuple is immutable so rating cannot be accidentally changed
#
# RETURNS: list of (rating, job_row) tuples sorted by rating descending
#          only jobs with rating > 0 are included
#
# -------------------------------------------------------
# 6. calculate_pagination(total_matched, requested_page_number_str)
# -------------------------------------------------------
# PURPOSE:
#   Calculate which page to show and which slice of results
#   to display. Ported from pagination logic in jobsearch.pl.
#   PAGE_SIZE = 16 same as demo.
#
# HOW TO IMPLEMENT:
#   Step 1 - Calculate total pages:
#     If total_matched == 0 set total_pages = 1
#     Otherwise:
#       total_pages = total_matched // PAGE_SIZE
#       If total_matched % PAGE_SIZE > 0 add 1 to total_pages
#       This handles leftover jobs that do not fill a full page
#
#   EXAMPLE:
#     40 jobs, PAGE_SIZE 16:
#     40 // 16 = 2 full pages
#     40 %  16 = 8 leftover jobs -> add 1 page
#     total_pages = 3
#
#   Step 2 - Parse requested page number:
#     Convert requested_page_number_str to integer
#     If conversion fails default to 1
#
#   Step 3 - Validate page number:
#     If requested_page < 1          -> current_page = 1
#     If requested_page > total_pages -> current_page = total_pages
#     Otherwise                       -> current_page = requested_page
#
#   Step 4 - Calculate start and end indexes:
#     start_index = PAGE_SIZE * (current_page - 1)
#     end_index   = start_index + PAGE_SIZE
#     These are used to slice rated_rows list in print_results_table()
#
#   EXAMPLE page 2:
#     start_index = 16 * (2-1) = 16
#     end_index   = 16 + 16   = 32
#     rated_rows[16:32] gives jobs 17 to 32
#
# RETURNS: current_page, total_pages, start_index, end_index
#
# -------------------------------------------------------
# 7. print_results_table(rated_rows, start_index,
#                        end_index, total_matched,
#                        query_string)
# -------------------------------------------------------
# PURPOSE:
#   Print the HTML results table showing one page of jobs.
#   Matches the demo's print_job() in jobsearch.pl and
#   print_result_rows() in ematch_class.cxx.
#
# HOW TO IMPLEMENT:
#   - Print centered heading showing total matches
#   - Print HTML table with border=1
#   - Print table header row with these 7 columns:
#     Job Number, Rating, Job Title, Special field,
#     Location, Company, Salary Range
#   - Slice the current page jobs: page_rows = rated_rows[start_index:end_index]
#   - Set job_number = start_index + 1
#     (so page 2 starts at 17 not 1 - same as demo)
#   - Loop through each (rating, job_row) in page_rows:
#     Build salary display string:
#       If MIN_SALARY and MAX_SALARY both 0 show "Not specified"
#       Otherwise show "80000 - 88000"
#     Build job title link URL pointing to getjob.py:
#       Pass id, job_title, specialty, location, company, salary in URL
#     Print table row with yellow background #FFFFCC same as demo
#     Print all 7 columns in order
#     Increment job_number by 1
#   - Close table tags
#
# RETURNS: nothing, prints HTML directly
#
# -------------------------------------------------------
# 8. print_pagination_links(current_page, total_pages,
#                           query_string)
# -------------------------------------------------------
# PURPOSE:
#   Print Next Page, Previous Page, and Goto page number
#   links below the results table.
#   Ported from pagination link logic in jobsearch.pl.
#
# HOW TO IMPLEMENT:
#   - Build base_url by joining script path with query_string
#     base_url = "/~netid/cgi-bin/jobsearch.py?" + query_string
#     This preserves all the user's search choices in every link
#
#   - Print current page indicator: (Page 2 of 3)
#
#   - Next Page link:
#     If current_page < total_pages:
#       next_page = current_page + 1
#       Print clickable link: base_url + "&requested_page_number=" + next_page
#     Else:
#       Print plain text "Next Page >" with no link
#
#   - Previous Page link:
#     If current_page > 1:
#       prev_page = current_page - 1
#       Print clickable link: base_url + "&requested_page_number=" + prev_page
#     Else:
#       Print plain text "< Previous Page" with no link
#
#   - Goto page numbers (only if total_pages > 1):
#     Loop page_number from 1 to total_pages:
#       If page_number == current_page:
#         Print plain text (not a link - already on this page)
#       Else:
#         Print clickable link: base_url + "&requested_page_number=" + page_number
#
# NOTE ON &requested_page_number:
#   This is appended to the original query string so when user
#   clicks Next Page, jobsearch.py runs again with the same
#   search filters but a different page number.
#
# RETURNS: nothing, prints HTML directly
#
# -------------------------------------------------------
# 9. print_error_page(error_message)
# -------------------------------------------------------
# PURPOSE:
#   Show a clean error page if something goes wrong at
#   the top level instead of showing a Python traceback.
#
# HOW TO IMPLEMENT:
#   - Print Content-Type header
#   - Print print_header()
#   - Print the error message in a readable format
#   - Print a link back to job_search.html
#   - Print print_footer()
#
# RETURNS: nothing, prints HTML directly
#
# -------------------------------------------------------
# 10. MAIN ENTRY POINT (at bottom of file, no function)
# -------------------------------------------------------
# PURPOSE:
#   This runs when the web server calls jobsearch.py.
#   Calls all the above functions in the correct order.
#
# HOW TO IMPLEMENT:
#   Wrap everything in try/except. Steps in order:
#
#   1. Print "Content-Type: text/html" and blank line
#      MUST be first before any other output
#
#   2. Call get_form_parameters() -> params
#
#   3. Call parse_salary(params["salary"]) -> min_salary_number
#
#   4. Figure out location value:
#      Read params["location_type"] to know which dropdown to use
#      If "region" -> location_value = params["region"]
#      If "state"  -> location_value = params["state"]
#      If "city"   -> location_value = params["city"]
#
#   5. Build search_params dictionary for rating.py:
#      job_type, location_type, location_value,
#      min_salary, company_name, keyword
#
#   6. Call build_sql_query(params) -> sql, binds
#
#   7. Call fetch_all_job_rows(sql, binds) -> job_rows
#
#   8. Call rate_and_sort_jobs(job_rows, search_params) -> rated_rows
#      total_matched = len(rated_rows)
#
#   9. Call calculate_pagination(total_matched,
#      params["requested_page_number"])
#      -> current_page, total_pages, start_index, end_index
#
#   10. Get query_string from os.environ.get("QUERY_STRING", "")
#       This is used for pagination links to preserve search filters
#
#   11. Call print_header("Job Search Results")
#
#   12. Call print_results_table(rated_rows, start_index,
#       end_index, total_matched, query_string)
#
#   13. Call print_pagination_links(current_page,
#       total_pages, query_string)
#
#   14. Call print_footer()
#
#   If any exception occurs call print_error_page()
#
# =======================================================