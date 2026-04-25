# =======================================================
# rating.py - IMPLEMENTATION GUIDE
# =======================================================
# This file contains all rating functions for the job
# search project. Read this guide carefully before
# implementing any function.
#
# DEPENDENT FILES:
#   This file imports from the following files.
#   Make sure these are implemented first before
#   touching this file:
#
#   1. lib/config.py
#      - JOB_TYPE_PENALTY  : 2D dictionary used by compute_job_type_rating()
#      - SIMILAR_COMPANIES : dictionary used by compute_company_rating()
#
#   2. lib/location_data.py
#      - REGION_COMPATIBILITY   : 17x17 matrix used by compute_region_rating()
#      - NEIGHBOR_STATE_RATINGS : dictionary used by compute_state_rating()
#      - NEIGHBOR_CITY_RATINGS  : dictionary used by compute_city_rating()
#      - STATES_IN_REGIONS      : dictionary used by check_if_state_in_region()
#      - CITY_TO_STATE          : dictionary used by city_is_in_state()
#      - find_region_index()    : function used by compute_region_rating()
#      - find_state_index()     : function used by compute_state_rating()
#      - find_city_index()      : function used by compute_city_rating()
#      - city_is_in_state()     : function used by check_if_city_in_region()
#
#   3. lib/db.py
#      - Not directly imported here but must be working
#        because jobsearch.py uses it to fetch job rows
#        which are then passed to compute_job_rating()
#
# =======================================================
# HOW RATING WORKS (read this first)
# =======================================================
# Every job starts with rating = 100
# Each function below returns a DEDUCTION (penalty number)
# The master function compute_job_rating() subtracts each
# deduction from 100 one by one
# If rating drops to 0 or below the job is excluded
# If rating stays above 0 the job is kept and sorted
# Higher rating = better match = appears higher in results
#
# =======================================================
# FUNCTIONS TO IMPLEMENT (in this order)
# =======================================================
#
# -------------------------------------------------------
# 1. check_if_state_in_region(state_index, region_index)
# -------------------------------------------------------
# PURPOSE:
#   Binary check - is this state inside this region?
#   Returns a number not a boolean because rating system
#   works with numbers only.
#
# HOW TO IMPLEMENT:
#   - Look up region_index in STATES_IN_REGIONS dictionary
#     which gives a list of all state indexes in that region
#   - Check if state_index is in that list
#   - If YES return 0 (no deduction - state is in region)
#   - If NO  return 100 (full deduction - state not in region)
#
# RETURNS: 0 or 100
#
# CALLED BY: compute_region_rating(), compute_state_rating()
#
# -------------------------------------------------------
# 2. check_if_city_in_region(city_index, region_index)
# -------------------------------------------------------
# PURPOSE:
#   Binary check - is this city inside any state in this region?
#   Used as a fallback when job has no region or state stored
#   but has a city.
#
# HOW TO IMPLEMENT:
#   - Get list of all states in the region from STATES_IN_REGIONS
#   - Loop through each state in that list
#   - For each state call city_is_in_state(city_index, state_index)
#   - If any state contains the city return 0 immediately and stop
#   - If loop finishes with no match return 100
#
# RETURNS: 0 or 100
#
# CALLED BY: compute_region_rating()
#
# -------------------------------------------------------
# 3. compute_salary_rating(asked_min_salary, job_min_salary)
# -------------------------------------------------------
# PURPOSE:
#   Calculate how much to penalize a job based on salary mismatch.
#   Ported EXACTLY from compute_sal_rating() in demo's ematch_class.cxx
#
# HOW TO IMPLEMENT:
#   - If asked_min_salary <= job_min_salary return 0
#     (job pays enough or more - no penalty)
#   - If asked_min_salary > job_min_salary use this formula:
#     percent   = (asked_min_salary - job_min_salary) / (asked_min_salary + 1)
#     deduction = int(percent * 100)
#   - Return deduction
#
# EXAMPLE:
#   User wants $80,000, job pays $60,000:
#   percent   = (80000 - 60000) / (80000 + 1) = 0.24
#   deduction = int(0.24 * 100) = 24
#
# RETURNS: integer between 0 and 100
#
# CALLED BY: compute_job_rating()
#
# -------------------------------------------------------
# 4. compute_region_rating(asked_region_index,
#                          job_region_name,
#                          job_state_name,
#                          job_city_name)
# -------------------------------------------------------
# PURPOSE:
#   Calculate location penalty when user searched by REGION.
#   Ported from compute_region_rating() in demo's ematch_class.cxx
#
# HOW TO IMPLEMENT:
#   Step 1 - Convert job location names to indexes:
#     job_region_index = find_region_index(job_region_name)
#     job_state_index  = find_state_index(job_state_name)
#     job_city_index   = find_city_index(job_city_name)
#
#   Step 2 - Three cases in priority order:
#
#   CASE 1 - Job has a region (job_region_index != -1):
#     Check REGION_COMPATIBILITY[job_region_index][asked_region_index]
#     - If result is 1 -> perfect match -> deduction = 0
#     - If result is 2 -> overlap -> deduction = 70
#       Then try to improve by checking state or city:
#       If job has state: call check_if_state_in_region()
#       If job has city:  call check_if_city_in_region()
#       Take the lower (better) of 70 and the check result
#     - If result is 0 -> no overlap -> deduction = 100
#
#   CASE 2 - Job has no region but has state (job_state_index != -1):
#     Call check_if_state_in_region(job_state_index, asked_region_index)
#     Use that as the deduction
#
#   CASE 3 - Job has no region or state but has city (job_city_index != -1):
#     Call check_if_city_in_region(job_city_index, asked_region_index)
#     Use that as the deduction
#
# RETURNS: integer between 0 and 100
#
# CALLED BY: compute_job_rating()
#
# -------------------------------------------------------
# 5. compute_state_rating(asked_state_index,
#                         job_region_name,
#                         job_state_name,
#                         job_city_name)
# -------------------------------------------------------
# PURPOSE:
#   Calculate location penalty when user searched by STATE.
#   Ported from compute_state_rating() in demo's ematch_class.cxx
#
# HOW TO IMPLEMENT:
#   Step 1 - Convert job location names to indexes:
#     job_region_index = find_region_index(job_region_name)
#     job_state_index  = find_state_index(job_state_name)
#     job_city_index   = find_city_index(job_city_name)
#
#   Step 2 - Three cases in priority order:
#
#   CASE 1 - Job has a state (job_state_index != -1):
#     Look up NEIGHBOR_STATE_RATINGS[asked_state_index]
#     This gives a list of (neighbor_state_index, penalty) pairs
#     Loop through the list looking for job_state_index
#     If found use that penalty as deduction
#     If not found deduction stays 100
#
#   CASE 2 - Job has no state but has city (job_city_index != -1):
#     Look up NEIGHBOR_STATE_RATINGS[asked_state_index]
#     Loop through the list of (neighbor_state_index, penalty) pairs
#     For each neighbor state call city_is_in_state(job_city_index, neighbor_state_index)
#     If city is in that state use that penalty as deduction and stop
#     If not found deduction stays 100
#
#   CASE 3 - Job has no state or city but has region (job_region_index != -1):
#     Set deduction = 30 (default penalty for region fallback)
#     Call check_if_state_in_region(asked_state_index, job_region_index)
#     Take the HIGHER (worse) of 30 and that result
#
# RETURNS: integer between 0 and 100
#
# CALLED BY: compute_job_rating()
#
# -------------------------------------------------------
# 6. compute_city_rating(asked_city_index, job_city_name)
# -------------------------------------------------------
# PURPOSE:
#   Calculate location penalty when user searched by CITY.
#   Ported from compute_city_rating() in demo's ematch_class.cxx
#
# HOW TO IMPLEMENT:
#   - If job has no city return 100 immediately
#   - Convert job city name to index using find_city_index()
#   - If city not found in our list return 100
#   - If exact match (asked city == job city) return 0
#   - Otherwise look up NEIGHBOR_CITY_RATINGS[asked_city_index]
#     This gives a list of (neighbor_city_index, penalty) pairs
#     Loop through looking for job_city_index
#     If found return that penalty
#     If not found return 100
#
# RETURNS: integer between 0 and 100
#
# CALLED BY: compute_job_rating()
#
# -------------------------------------------------------
# 7. compute_job_type_rating(asked_job_type, job_type)
# -------------------------------------------------------
# PURPOSE:
#   PROJECT FEATURE 1
#   Calculate penalty based on job type mismatch.
#   The demo used job_type as exact WHERE clause filter.
#   We changed it to a rating system so ALL jobs are returned
#   and penalized based on how far their type is from asked type.
#
# HOW TO IMPLEMENT:
#   - If asked_job_type is None, empty, or "All" return 0 (no penalty)
#   - Convert both asked_job_type and job_type to lowercase
#   - Look up JOB_TYPE_PENALTY[asked_lower][job_lower]
#     This gives the penalty number directly
#   - If asked type not in table return 0
#   - If job type not in asked type's row return 30 (default penalty)
#   - Return the penalty found
#
# EXAMPLE:
#   User asked "regular", job is "intern":
#   JOB_TYPE_PENALTY["regular"]["intern"] = 40
#   Return 40
#
# RETURNS: integer between 0 and 100
#
# CALLED BY: compute_job_rating()
#
# -------------------------------------------------------
# 8. compute_company_rating(asked_company, job_company)
# -------------------------------------------------------
# PURPOSE:
#   PROJECT FEATURE 2 AND FEATURE 3
#   Feature 2: Calculate penalty based on company mismatch
#   Feature 3: Also return similar companies with a penalty
#   The demo used company_name as exact WHERE clause filter.
#   We changed it so ALL companies are returned and rated.
#
# HOW TO IMPLEMENT:
#   - If asked_company is None, empty, or "All" return 0 (no penalty)
#   - Strip and compare asked_company and job_company (case insensitive)
#   - If exact match return 0 (perfect score)
#   - If not exact match look up SIMILAR_COMPANIES[asked_company]
#     This gives a list of (similar_company, penalty) pairs
#     Loop through looking for job_company (case insensitive)
#     If found return that penalty (Feature 3 - similar company)
#   - If not found in similar list either return 60
#     (unrelated company - still shown but near bottom)
#
# EXAMPLE:
#   User asked "Intel", job is "AMD":
#   SIMILAR_COMPANIES["Intel"] contains ("AMD", 15)
#   Return 15
#
#   User asked "Intel", job is "Dell":
#   Dell not in Intel's similar list
#   Return 60
#
# RETURNS: integer between 0 and 100
#
# CALLED BY: compute_job_rating()
#
# -------------------------------------------------------
# 9. compute_keyword_rating(keyword, job_title,
#                           job_specialization,
#                           job_description,
#                           job_qualification)
# -------------------------------------------------------
# PURPOSE:
#   PROJECT FEATURE 4
#   Search for keyword across four job text fields.
#   This feature was in the HTML form but never implemented
#   in the demo backend. We implement it here.
#
# HOW TO IMPLEMENT:
#   - If keyword is None or empty return 0 (no penalty)
#   - Convert keyword to lowercase
#   - Search each field in this priority order:
#     1. JOB_TITLE        -> if keyword found return 0  (best match)
#     2. SPECIALIZATION   -> if keyword found return 0  (best match)
#     3. DESCRIPTION      -> if keyword found return 10 (good match)
#     4. QUALIFICATION    -> if keyword found return 15 (ok match)
#   - If not found in any field return 100 (exclude job)
#   - All searches must be case insensitive
#   - Use substring search (keyword anywhere in the field counts)
#
# EXAMPLE:
#   keyword = "database"
#   job_title = "Database Administrator" -> found in title -> return 0
#
#   keyword = "database"
#   job_title = "Engineer"
#   job_description = "Must have database experience" -> found in desc -> return 10
#
# RETURNS: integer between 0 and 100
#
# CALLED BY: compute_job_rating()
#
# -------------------------------------------------------
# 10. compute_job_rating(job_row, search_params)
# -------------------------------------------------------
# PURPOSE:
#   MASTER FUNCTION - called once per job row from jobsearch.py
#   Combines all individual rating functions into one final score.
#   Ported from compute_a_job_rating() in demo's ematch_class.cxx
#   Extended with four new project features.
#
# HOW TO IMPLEMENT:
#   - Start with rating = 100
#   - Call each rating function below in this order:
#     1. compute_job_type_rating()  -> Feature 1
#     2. compute_region_rating()    -> location (if user searched by region)
#        OR compute_state_rating()  -> location (if user searched by state)
#        OR compute_city_rating()   -> location (if user searched by city)
#     3. compute_salary_rating()    -> salary
#     4. compute_company_rating()   -> Features 2 and 3
#     5. compute_keyword_rating()   -> Feature 4
#   - After each function subtract its deduction from rating
#   - After each subtraction check if rating <= 0
#     If yes return 0 immediately (exclude job, stop checking)
#   - Skip a function entirely if user selected "All" or left it empty
#   - Return final rating at the end
#
# PARAMETERS:
#   job_row -- dictionary from database with keys:
#     JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION,
#     REGION_NAME, STATE_NAME, LOCATION,
#     MIN_SALARY, MAX_SALARY, COMPANY_NAME,
#     DESCRIPTION, QUALIFICATION
#
#   search_params -- dictionary from jobsearch.py with keys:
#     job_type, location_type, location_value,
#     min_salary, company_name, keyword
#
# RETURNS: integer between 0 and 100
#          0 means job is excluded from results
#
# CALLED BY: rate_and_sort_jobs() in jobsearch.py
#
# =======================================================