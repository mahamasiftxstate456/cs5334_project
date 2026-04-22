# =======================================================
# getjob.py - IMPLEMENTATION GUIDE
# =======================================================
# This is the job detail page. It shows full information
# about a single job when user clicks a job title link
# in the search results page.
#
# This is an IMPROVED version of the demo's getjob.pl.
# The demo read job details from URL parameters only and
# DESCRIPTION was never shown (assigned but never fetched).
# Our version queries the database using job_id to fetch
# the complete job row including DESCRIPTION and QUALIFICATION.
#
# HOW IT IS CALLED:
#   User clicks job title link in print_results_table()
#   The link URL looks like:
#   /~netid/cgi-bin/getjob.py?id=000000001&job_title=Manager&...
#
# DEPENDENT FILES:
#   Make sure these are implemented and working first:
#
#   1. lib/db.py
#      - get_connection() : used by fetch_job_by_id()
#        to connect to Oracle database
#
#   2. cgi-bin/common.py
#      - print_header() : used to print HTML page header
#      - print_footer() : used to print HTML page footer
#
#   3. cgi-bin/jobsearch.py
#      - print_results_table() must build the job link
#        pointing to getjob.py with ?id= in the URL
#
# =======================================================
# FUNCTIONS TO IMPLEMENT (in this order)
# =======================================================
#
# -------------------------------------------------------
# 1. get_job_id()
# -------------------------------------------------------
# PURPOSE:
#   Read the job id from the URL parameters.
#   The job title link passes job_id as ?id=000000001
#
# HOW TO IMPLEMENT:
#   - Use cgi.FieldStorage() to read the GET request
#   - Look for field named "id" in the form
#   - If found and not empty return its value stripped of spaces
#   - If not found return None
#
# RETURNS: job_id string or None if not in URL
#
# -------------------------------------------------------
# 2. fetch_job_by_id(job_id)
# -------------------------------------------------------
# PURPOSE:
#   Query the database for the FULL job row using job_id.
#   This is the main improvement over demo's getjob.pl
#   which never queried the database at all.
#
# HOW TO IMPLEMENT:
#   - Call get_connection() to open database connection
#   - Write SQL query:
#     SELECT JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION,
#     COUNTRY_CODE, REGION_NAME, STATE_NAME, LOCATION,
#     MIN_SALARY, MAX_SALARY, COMPANY_NAME, START_DATE,
#     REFERENCE_NUM, CONTACT_PERSON, DESCRIPTION, QUALIFICATION
#     FROM job
#     WHERE JOB_ID = :job_id
#     Use bind variable :job_id to prevent SQL injection
#   - Execute query and fetch ONE row using cursor.fetchone()
#   - If row found convert to named dictionary same as jobsearch.py:
#     Use safe_str() for text columns
#     Use safe_int() for number columns (COUNTRY_CODE, MIN_SALARY, MAX_SALARY)
#   - If row not found return None
#   - Wrap in try/except/finally, always close cursor and connection
#   - Return the job dictionary or None
#
# RETURNS: job dictionary with all columns, or None if not found
#
# -------------------------------------------------------
# 3. print_job_detail(job)
# -------------------------------------------------------
# PURPOSE:
#   Print the full job detail page matching the demo's
#   getjob.pl UI exactly. Green color #006600 for all
#   values same as demo.
#
# HOW TO IMPLEMENT:
#   - Build salary display string:
#     If MIN_SALARY and MAX_SALARY both 0 show "Not specified"
#     Otherwise show "80000 - 88000"
#
#   - Print page heading: <h2>Job description</h2>
#
#   - Print form tag pointing to submit_resume.pl
#     (submit_resume.pl was never provided in demo
#      so keep same placeholder as demo)
#
#   - Print these job fields with green color #006600:
#     Job Title        -> JOB_TITLE
#     Job Type         -> JOB_TYPE         (not in demo, we added this)
#     Specialized area -> SPECIALIZATION
#     Location         -> LOCATION + STATE_NAME combined
#     Company          -> COMPANY_NAME
#     Salary Range     -> salary display string
#     Start Date       -> START_DATE        (not in demo, we added this)
#     Contact Person   -> CONTACT_PERSON    (not in demo, we added this)
#     Reference Number -> REFERENCE_NUM     (not in demo, we added this)
#
#   - Print Job Description section:
#     This is the KEY IMPROVEMENT over demo's getjob.pl
#     The demo used $description but never assigned it
#     We fetch it from database and display it properly
#     If DESCRIPTION is empty show "No description available."
#
#   - Print Qualification section:
#     Also not shown in demo - we added this
#     If QUALIFICATION is empty show "No qualification details available."
#
#   - Print resume textarea:
#     Same as demo - rows=20, cols=60
#     Add hidden field with job_id for the submit form
#     Submit button same text as demo
#
#   - Close form tag
#
# RETURNS: nothing, prints HTML directly
#
# -------------------------------------------------------
# 4. print_not_found_page(job_id)
# -------------------------------------------------------
# PURPOSE:
#   Show a simple page when job_id is not found in database.
#
# HOW TO IMPLEMENT:
#   - Print a message saying job was not found
#   - Include the job_id in the message
#   - Print a link back to job_search.html
#
# RETURNS: nothing, prints HTML directly
#
# -------------------------------------------------------
# 5. print_no_id_page()
# -------------------------------------------------------
# PURPOSE:
#   Show a simple page when no job_id was provided in URL.
#   Handles case where someone opens getjob.py directly
#   without clicking a job title link.
#
# HOW TO IMPLEMENT:
#   - Print a message saying no job was selected
#   - Print a link back to job_search.html
#
# RETURNS: nothing, prints HTML directly
#
# -------------------------------------------------------
# 6. print_error_page(error_message)
# -------------------------------------------------------
# PURPOSE:
#   Show a clean error page if something goes critically
#   wrong before or during the database query.
#
# HOW TO IMPLEMENT:
#   - Print Content-Type header
#   - Print print_header()
#   - Print the error message
#   - Print a link back to job_search.html
#   - Print print_footer()
#
# RETURNS: nothing, prints HTML directly
#
# -------------------------------------------------------
# 7. MAIN ENTRY POINT (at bottom of file, no function)
# -------------------------------------------------------
# PURPOSE:
#   This runs when the web server calls getjob.py.
#   Calls all the above functions in the correct order.
#
# HOW TO IMPLEMENT:
#   Wrap everything in try/except. Steps in order:
#
#   1. Print "Content-Type: text/html" and blank line
#      MUST be first before any other output
#
#   2. Call print_header("Job Description")
#
#   3. Call get_job_id() -> job_id
#
#   4. If job_id is None:
#        Call print_no_id_page()
#      Else:
#        Call fetch_job_by_id(job_id) -> job
#        If job is None:
#          Call print_not_found_page(job_id)
#        Else:
#          Call print_job_detail(job)
#
#   5. Call print_footer()
#
#   If any exception occurs call print_error_page()
#
# =======================================================