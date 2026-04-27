#!/usr/bin/env python3
"""
lib/rating.py
-------------
Rating engine for the job search project.

Every job starts with a base score of 100. Each rating function below
returns a DEDUCTION (a penalty to subtract). The master function
compute_job_rating() applies all applicable deductions and returns the
final score. Jobs with a final score <= 0 are excluded from results.

Implements all four project features:
  Feature 1 - Job type rating    : compute_job_type_rating()
  Feature 2 - Company rating     : compute_company_rating()
  Feature 3 - Similar companies  : compute_company_rating() (same function)
  Feature 4 - Keyword search     : compute_keyword_rating()

Location and salary rating are ported from the demo's ematch_class.cxx:
  compute_region_rating(), compute_state_rating(), compute_city_rating()
  compute_salary_rating()

Depends on:
  lib/config.py        -> JOB_TYPE_PENALTY, SIMILAR_COMPANIES
  lib/location_data.py -> all lookup tables and helper functions
"""

import sys
import os

# Add project root to path so imports work when called from cgi-bin
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.config import JOB_TYPE_PENALTY, SIMILAR_COMPANIES
from lib.location_data import (
    REGION_COMPATIBILITY,
    NEIGHBOR_STATE_RATINGS,
    NEIGHBOR_CITY_RATINGS,
    STATES_IN_REGIONS,
    find_region_index,
    find_state_index,
    find_city_index,
    city_is_in_state,
)


# =============================================================
# LOCATION HELPER FUNCTIONS
# =============================================================

def check_if_state_in_region(state_index, region_index):
    """
    Binary check: is this state inside this region?

    Looks up region_index in STATES_IN_REGIONS to get the list of all
    state indexes belonging to that region, then checks membership.
    Returns a number (not bool) because the rating system works
    entirely with numeric deductions.

    Parameters:
        state_index  (int) -- index of the state to check
        region_index (int) -- index of the region to check against

    Returns:
        0   if the state IS in the region (no deduction)
        100 if the state is NOT in the region (full deduction)

    Called by: compute_region_rating(), compute_state_rating()
    """
    states_in_region = STATES_IN_REGIONS.get(region_index, [])
    if state_index in states_in_region:
        return 0
    return 100


def check_if_city_in_region(city_index, region_index):
    """
    Binary check: is this city inside any state that belongs to this region?

    Used as a fallback when a job row has no region or state stored but
    does have a city. Iterates through every state in the region and
    calls city_is_in_state() for each one.

    Parameters:
        city_index   (int) -- index of the city to check
        region_index (int) -- index of the region to check against

    Returns:
        0   if the city belongs to a state that is in the region
        100 if the city does not belong to any state in the region

    Called by: compute_region_rating()
    """
    states_in_region = STATES_IN_REGIONS.get(region_index, [])
    for state_index in states_in_region:
        if city_is_in_state(city_index, state_index):
            return 0
    return 100


# =============================================================
# SALARY RATING  (ported from demo's compute_sal_rating())
# =============================================================

def compute_salary_rating(asked_min_salary, job_min_salary):
    """
    Calculate the penalty for a salary mismatch.

    Ported exactly from compute_sal_rating() in ematch_class.cxx.
    If the job pays at least what the user asked for there is no
    penalty. If it pays less, the penalty is proportional to how
    far short it falls.

    Formula when job pays less than asked:
        percent   = (asked - job) / (asked + 1)
        deduction = int(percent * 100)

    The +1 in the divisor prevents division by zero when asked == 0,
    and matches the demo's implementation exactly.

    Example:
        User wants $80,000, job pays $60,000:
        percent   = (80000 - 60000) / (80000 + 1) = 0.24999...
        deduction = int(0.24999 * 100) = 24

    Parameters:
        asked_min_salary (int) -- minimum salary the user requested (0 = no filter)
        job_min_salary   (int) -- minimum salary listed on the job (0 = not specified)

    Returns:
        int deduction between 0 and 99
        0 means no penalty (job pays enough, or no salary filter was set)

    Called by: compute_job_rating()
    """
    if asked_min_salary <= job_min_salary:
        return 0

    percent   = (asked_min_salary - job_min_salary) / (asked_min_salary + 1)
    deduction = int(percent * 100)
    return deduction


# =============================================================
# LOCATION RATING  (ported from demo's ematch_class.cxx)
# =============================================================

def compute_region_rating(asked_region_index, job_region_name, job_state_name, job_city_name):
    """
    Calculate the location penalty when the user searched by REGION.

    Ported from compute_region_rating() in ematch_class.cxx.

    Tries three cases in priority order depending on what location
    data the job row actually has:

      Case 1 - Job has a region:
        Consult REGION_COMPATIBILITY[job_region][asked_region].
        1 = contained -> deduction 0
        2 = overlap   -> deduction 70, then try to improve via state/city
        0 = no match  -> deduction 100

      Case 2 - Job has no region but has a state:
        Call check_if_state_in_region() -> 0 or 100

      Case 3 - Job has no region or state but has a city:
        Call check_if_city_in_region() -> 0 or 100

    Parameters:
        asked_region_index (int) -- index of the region the user searched for
        job_region_name    (str) -- REGION_NAME value from the job row
        job_state_name     (str) -- STATE_NAME value from the job row
        job_city_name      (str) -- LOCATION value from the job row

    Returns:
        int deduction between 0 and 100

    Called by: compute_job_rating()
    """
    job_region_index = find_region_index(job_region_name)
    job_state_index  = find_state_index(job_state_name)
    job_city_index   = find_city_index(job_city_name)

    # Case 1: job has a recognisable region
    if job_region_index != -1:
        compatibility = REGION_COMPATIBILITY[job_region_index][asked_region_index]

        if compatibility == 1:
            # Job region is contained within (or equal to) the asked region
            return 0

        elif compatibility == 2:
            # Regions overlap - start with a 70-point penalty but try to
            # improve it using more specific location data
            deduction = 70
            if job_state_index != -1:
                state_check = check_if_state_in_region(job_state_index, asked_region_index)
                deduction   = min(deduction, state_check)
            elif job_city_index != -1:
                city_check = check_if_city_in_region(job_city_index, asked_region_index)
                deduction  = min(deduction, city_check)
            return deduction

        else:
            # compatibility == 0: no overlap at all
            return 100

    # Case 2: no region stored, but the job has a state
    if job_state_index != -1:
        return check_if_state_in_region(job_state_index, asked_region_index)

    # Case 3: no region or state, but the job has a city
    if job_city_index != -1:
        return check_if_city_in_region(job_city_index, asked_region_index)

    # No usable location data on the job at all
    return 100


def compute_state_rating(asked_state_index, job_region_name, job_state_name, job_city_name):
    """
    Calculate the location penalty when the user searched by STATE.

    Ported from compute_state_rating() in ematch_class.cxx.

    Tries three cases in priority order:

      Case 1 - Job has a state:
        Look up NEIGHBOR_STATE_RATINGS[asked_state_index] and scan for
        the job's state. Uses the penalty from the neighbor table (0 for
        exact match, 20-50 for neighboring states, 100 if not found).

      Case 2 - Job has no state but has a city:
        For each neighbor state in NEIGHBOR_STATE_RATINGS[asked_state_index],
        check whether the job city belongs to that state via city_is_in_state().
        Use that neighbor's penalty if a match is found.

      Case 3 - Job has no state or city but has a region:
        Default deduction = 30. Call check_if_state_in_region() and take
        the HIGHER (worse) of 30 and that result.

    Parameters:
        asked_state_index (int) -- index of the state the user searched for
        job_region_name   (str) -- REGION_NAME value from the job row
        job_state_name    (str) -- STATE_NAME value from the job row
        job_city_name     (str) -- LOCATION value from the job row

    Returns:
        int deduction between 0 and 100

    Called by: compute_job_rating()
    """
    job_region_index = find_region_index(job_region_name)
    job_state_index  = find_state_index(job_state_name)
    job_city_index   = find_city_index(job_city_name)

    neighbors = NEIGHBOR_STATE_RATINGS.get(asked_state_index, [])

    # Case 1: job has a recognisable state
    if job_state_index != -1:
        for (neighbor_state_index, penalty) in neighbors:
            if neighbor_state_index == job_state_index:
                return penalty
        return 100

    # Case 2: no state stored, but the job has a city
    if job_city_index != -1:
        for (neighbor_state_index, penalty) in neighbors:
            if city_is_in_state(job_city_index, neighbor_state_index):
                return penalty
        return 100

    # Case 3: no state or city, but the job has a region
    if job_region_index != -1:
        deduction    = 30
        region_check = check_if_state_in_region(asked_state_index, job_region_index)
        return max(deduction, region_check)

    # No usable location data on the job at all
    return 100


def compute_city_rating(asked_city_index, job_city_name):
    """
    Calculate the location penalty when the user searched by CITY.

    Ported from compute_city_rating() in ematch_class.cxx.

    Steps:
      1. If the job has no city name, return 100 immediately.
      2. Convert the job city name to an index; return 100 if not found.
      3. Exact match -> return 0.
      4. Look up NEIGHBOR_CITY_RATINGS[asked_city_index] and scan for
         the job city. Return that penalty if found, 100 otherwise.

    Parameters:
        asked_city_index (int) -- index of the city the user searched for
        job_city_name    (str) -- LOCATION value from the job row

    Returns:
        int deduction between 0 and 100

    Called by: compute_job_rating()
    """
    # No city stored on the job
    if not job_city_name or not job_city_name.strip():
        return 100

    job_city_index = find_city_index(job_city_name)

    # City name not in our lookup table
    if job_city_index == -1:
        return 100

    # Exact match
    if job_city_index == asked_city_index:
        return 0

    # Check neighbor list for the asked city
    neighbors = NEIGHBOR_CITY_RATINGS.get(asked_city_index, [])
    for (neighbor_city_index, penalty) in neighbors:
        if neighbor_city_index == job_city_index:
            return penalty

    return 100


# =============================================================
# PROJECT FEATURE 1 - JOB TYPE RATING
# =============================================================

def compute_job_type_rating(asked_job_type, job_type):
    """
    Calculate the penalty for a job type mismatch.  (Project Feature 1)

    The demo added job_type to the SQL WHERE clause, returning only exact
    matches. This function replaces that with a rating system so ALL job
    types are returned but penalised based on how far they are from what
    the user asked for.

    Penalty values come from JOB_TYPE_PENALTY in lib/config.py.
    Both keys use underscores for multi-word types (e.g. "entry_level").
    If the asked type is not in the table (e.g. "All"), no penalty is
    applied. If the job type is not in the inner row, a default penalty
    of 30 is used.

    Example:
        User asked "regular", job is "intern":
        JOB_TYPE_PENALTY["regular"]["intern"] = 40  -> return 40

    Parameters:
        asked_job_type (str) -- job type from the search form (may be "All"/empty)
        job_type       (str) -- JOB_TYPE value from the job row

    Returns:
        int deduction between 0 and 100
        0 means no penalty (no filter set, or exact match)

    Called by: compute_job_rating()
    """
    if not asked_job_type or asked_job_type.strip().lower() in ("", "all"):
        return 0

    asked_lower = asked_job_type.strip().lower()
    job_lower   = job_type.strip().lower() if job_type else ""

    # Asked type not in penalty table - no penalty
    if asked_lower not in JOB_TYPE_PENALTY:
        return 0

    inner_row = JOB_TYPE_PENALTY[asked_lower]

    # Job type is in the penalty table for this asked type
    if job_lower in inner_row:
        return inner_row[job_lower]

    # Job type exists but is not represented in the row - apply default
    return 30


# =============================================================
# PROJECT FEATURES 2 & 3 - COMPANY RATING + SIMILAR COMPANIES
# =============================================================

def compute_company_rating(asked_company, job_company):
    """
    Calculate the penalty for a company mismatch.  (Project Features 2 & 3)

    Feature 2: The demo added company_name to the SQL WHERE clause,
    returning only exact matches. This function replaces that so ALL
    companies are returned, with non-matching companies penalised.

    Feature 3: Jobs from companies similar to the asked company are
    returned with a reduced penalty instead of the full 60-point
    default. Similarity data comes from SIMILAR_COMPANIES in config.py.

    Lookup is case-insensitive for both asked and job company. The
    SIMILAR_COMPANIES keys use title-case (e.g. "IBM", "Apple Computers")
    matching the COMPANIES dropdown list in config.py.

    Example:
        User asked "Intel", job is "AMD":
        SIMILAR_COMPANIES["Intel"] contains ("AMD", 15) -> return 15

        User asked "Intel", job is "Dell":
        Dell not in Intel's similar list -> return 60

    Parameters:
        asked_company (str) -- company name from the search form (may be "All"/empty)
        job_company   (str) -- COMPANY_NAME value from the job row

    Returns:
        int deduction between 0 and 100
        0 means no penalty (no filter set, or exact match)

    Called by: compute_job_rating()
    """
    if not asked_company or asked_company.strip().lower() in ("", "all"):
        return 0

    asked_stripped = asked_company.strip()
    job_stripped   = job_company.strip() if job_company else ""

    # Exact match (case insensitive)
    if asked_stripped.lower() == job_stripped.lower():
        return 0

    # Look for the asked company in the similarity table.
    # SIMILAR_COMPANIES keys are title-case; try the original string first,
    # then scan keys case-insensitively as a fallback.
    similar_list = SIMILAR_COMPANIES.get(asked_stripped, None)
    if similar_list is None:
        for key in SIMILAR_COMPANIES:
            if key.lower() == asked_stripped.lower():
                similar_list = SIMILAR_COMPANIES[key]
                break

    if similar_list:
        for (similar_name, penalty) in similar_list:
            if similar_name.lower() == job_stripped.lower():
                return penalty

    # Unrelated company - shown near the bottom of results
    return 60


# =============================================================
# PROJECT FEATURE 4 - KEYWORD SEARCH
# =============================================================

def compute_keyword_rating(keyword, job_title, job_specialization, job_description, job_qualification):
    """
    Calculate the penalty based on keyword relevance.  (Project Feature 4)

    The HTML search form has always had a keyword field, but the demo
    backend never processed it. This function implements the full
    keyword-matching pipeline.

    The keyword is searched across four fields in priority order.
    Finding it in a higher-priority field gives a lower deduction
    (better score):

        JOB_TITLE / SPECIALIZATION -> 0  (best: keyword defines the role)
        DESCRIPTION                -> 10 (good: keyword appears in body)
        QUALIFICATION              -> 15 (ok:   keyword appears in requirements)
        Not found anywhere         -> 100 (job excluded from results)

    All comparisons are case-insensitive substring searches.

    Example:
        keyword = "database", job_title = "Database Administrator"
        -> found in title -> return 0

        keyword = "database", job_title = "Engineer",
        job_description = "Must have database experience"
        -> found in description -> return 10

    Parameters:
        keyword            (str) -- keyword from the search form (may be None/empty)
        job_title          (str) -- JOB_TITLE value from the job row
        job_specialization (str) -- SPECIALIZATION value from the job row
        job_description    (str) -- DESCRIPTION value from the job row
        job_qualification  (str) -- QUALIFICATION value from the job row

    Returns:
        int deduction between 0 and 100
        0   means no penalty (no keyword entered, or found in title/specialization)
        100 means job is excluded (keyword not found anywhere)

    Called by: compute_job_rating()
    """
    if not keyword or not keyword.strip():
        return 0

    kw = keyword.strip().lower()

    # Normalise all fields to lowercase strings, treating None as ""
    title = (job_title          or "").lower()
    spec  = (job_specialization or "").lower()
    desc  = (job_description    or "").lower()
    qual  = (job_qualification  or "").lower()

    if kw in title or kw in spec:
        return 0

    if kw in desc:
        return 10

    if kw in qual:
        return 15

    # Keyword not found in any field - exclude this job
    return 100


# =============================================================
# MASTER RATING FUNCTION
# =============================================================

def compute_job_rating(job_row, search_params):
    """
    Compute the final match rating for a single job row.  (Master function)

    Ported from compute_a_job_rating() in ematch_class.cxx and extended
    with the four project features.

    Starts at 100 and subtracts deductions from each applicable rating
    function. If the running total drops to 0 or below at any point,
    returns 0 immediately (early exit) so the job is excluded without
    wasting time on the remaining checks.

    Deductions are applied in this order:
        1. Job type       (Feature 1)
        2. Location       (region / state / city - whichever the user chose)
        3. Salary
        4. Company name   (Features 2 & 3)
        5. Keyword        (Feature 4)

    A rating function is skipped entirely if the user left that field as
    "All" / empty, which means search_params will hold "" or "All" for it.

    Parameters:
        job_row (dict) -- one row from the Oracle job table, with keys:
            JOB_ID, JOB_TYPE, JOB_TITLE, SPECIALIZATION,
            REGION_NAME, STATE_NAME, LOCATION,
            MIN_SALARY, MAX_SALARY, COMPANY_NAME,
            DESCRIPTION, QUALIFICATION

        search_params (dict) -- parsed CGI parameters from jobsearch.py, with keys:
            job_type       (str)  -- "regular" / "intern" / ... / "" for no filter
            location_type  (str)  -- "region" / "state" / "city"
            location_value (str)  -- the actual region/state/city name, or "" for none
            min_salary     (int)  -- minimum salary number (0 = no filter)
            company_name   (str)  -- company name, or "" for no filter
            keyword        (str)  -- keyword string, or "" for none

    Returns:
        int between 0 and 100
        0 means the job should be excluded from results

    Called by: rate_and_sort_jobs() in jobsearch.py
    """
    rating = 100

    # ----------------------------------------------------------
    # 1. Job type rating  (Feature 1)
    # ----------------------------------------------------------
    asked_job_type = search_params.get("job_type", "")
    if asked_job_type and asked_job_type.lower() not in ("", "all"):
        deduction = compute_job_type_rating(asked_job_type, job_row.get("JOB_TYPE", ""))
        rating -= deduction
        if rating <= 0:
            return 0

    # ----------------------------------------------------------
    # 2. Location rating  (region / state / city)
    # ----------------------------------------------------------
    location_type  = search_params.get("location_type",  "")
    location_value = search_params.get("location_value", "")

    if location_value and location_value.lower() not in ("", "all", "any"):

        job_region_name = job_row.get("REGION_NAME", "")
        job_state_name  = job_row.get("STATE_NAME",  "")
        job_city_name   = job_row.get("LOCATION",    "")

        if location_type == "region":
            asked_region_index = find_region_index(location_value)
            if asked_region_index != -1:
                deduction = compute_region_rating(
                    asked_region_index, job_region_name, job_state_name, job_city_name
                )
                rating -= deduction
                if rating <= 0:
                    return 0

        elif location_type == "state":
            asked_state_index = find_state_index(location_value)
            if asked_state_index != -1:
                deduction = compute_state_rating(
                    asked_state_index, job_region_name, job_state_name, job_city_name
                )
                rating -= deduction
                if rating <= 0:
                    return 0

        elif location_type == "city":
            asked_city_index = find_city_index(location_value)
            if asked_city_index != -1:
                deduction = compute_city_rating(asked_city_index, job_city_name)
                rating -= deduction
                if rating <= 0:
                    return 0

    # ----------------------------------------------------------
    # 3. Salary rating
    # ----------------------------------------------------------
    min_salary = search_params.get("min_salary", 0)
    if min_salary and min_salary > 0:
        deduction = compute_salary_rating(min_salary, job_row.get("MIN_SALARY", 0))
        rating -= deduction
        if rating <= 0:
            return 0

    # ----------------------------------------------------------
    # 4. Company rating  (Features 2 & 3)
    # ----------------------------------------------------------
    asked_company = search_params.get("company_name", "")
    if asked_company and asked_company.lower() not in ("", "all"):
        deduction = compute_company_rating(asked_company, job_row.get("COMPANY_NAME", ""))
        rating -= deduction
        if rating <= 0:
            return 0

    # ----------------------------------------------------------
    # 5. Keyword rating  (Feature 4)
    # ----------------------------------------------------------
    keyword = search_params.get("keyword", "")
    if keyword and keyword.strip():
        deduction = compute_keyword_rating(
            keyword,
            job_row.get("JOB_TITLE",      ""),
            job_row.get("SPECIALIZATION", ""),
            job_row.get("DESCRIPTION",    ""),
            job_row.get("QUALIFICATION",  ""),
        )
        rating -= deduction
        if rating <= 0:
            return 0

    return rating
