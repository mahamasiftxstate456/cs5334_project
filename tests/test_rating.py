#!/usr/bin/env python3
"""
test_rating.py
-------------
Standalone tests for rating.py

Run from the cs5334_finalproject root directory:
    python3 tests/test_rating.py

All dependencies (lib/config.py and lib/location_data.py) must be implemented before running these tests.
"""

import sys
import os

# Folder structure:
#   cs5334_finalproject/
#       tests/          <- this file lives here
#       python/
#           lib/        <- rating.py, config.py, location_data.py live here
#           cgi-bin/
#
# Add python/ to path so "from lib.config import" works inside rating.py
# Add python/lib/ to path so "from rating import" works in this test file
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "python", "lib"))

from rating import (
    check_if_state_in_region,
    check_if_city_in_region,
    compute_salary_rating,
    compute_job_type_rating,
    compute_company_rating,
    compute_keyword_rating,
    compute_region_rating,
    compute_state_rating,
    compute_city_rating,
    compute_job_rating,
)
from location_data import  find_region_index, find_state_index, find_city_index

print ("=" * 60)
print("test_rating.py")
print("=" * 60)

## --- Salary ---
assert compute_salary_rating(0,      0)      == 0,  "salary: no filter"
assert compute_salary_rating(80000,  80000)  == 0,  "salary: exact match"
assert compute_salary_rating(80000,  100000) == 0,  "salary: job pays more"
assert compute_salary_rating(80000,  60000)  == 24, "salary: job pays less"
assert compute_salary_rating(50000,  0)      == 99, "salary: job pays nothing"
print("PASS  compute_salary_rating")
 
# --- Job type ---
assert compute_job_type_rating("",          "regular")     == 0,  "job_type: no filter"
assert compute_job_type_rating("All",       "intern")      == 0,  "job_type: All"
assert compute_job_type_rating("regular",   "regular")     == 0,  "job_type: exact"
assert compute_job_type_rating("regular",   "entry_level") == 20, "job_type: entry close"
assert compute_job_type_rating("regular",   "intern")      == 40, "job_type: intern far"
assert compute_job_type_rating("intern",    "co-op")       == 10, "job_type: intern/co-op similar"
assert compute_job_type_rating("intern",    "regular")     == 50, "job_type: intern/regular far"
assert compute_job_type_rating("unknown",   "regular")     == 0,  "job_type: unknown asked type"
assert compute_job_type_rating("regular",   "unknown")     == 30, "job_type: unknown job type default"
print("PASS  compute_job_type_rating")
 
# --- Company ---
assert compute_company_rating("",             "IBM")      == 0,  "company: no filter"
assert compute_company_rating("All",          "IBM")      == 0,  "company: All"
assert compute_company_rating("IBM",          "IBM")      == 0,  "company: exact"
assert compute_company_rating("IBM",          "ibm")      == 0,  "company: case insensitive exact"
assert compute_company_rating("Intel",        "AMD")      == 15, "company: similar (Intel/AMD)"
assert compute_company_rating("Intel",        "Dell")     == 60, "company: unrelated"
assert compute_company_rating("IBM",          "Dell")     == 20, "company: similar (IBM/Dell)"
assert compute_company_rating("IBM",          "RandomCo") == 60, "company: unknown job company"
print("PASS  compute_company_rating")
 
# --- Keyword ---
assert compute_keyword_rating("",         "Engineer", "DB Admin", "desc", "qual") == 0,   "kw: empty"
assert compute_keyword_rating("database", "Database Administrator", "", "", "")   == 0,   "kw: in title"
assert compute_keyword_rating("oracle",   "Engineer", "Oracle DBA", "", "")       == 0,   "kw: in spec"
assert compute_keyword_rating("python",   "Engineer", "Java Dev", "Python scripts", "") == 10, "kw: in desc"
assert compute_keyword_rating("agile",    "Engineer", "Java Dev", "waterfall", "Must know Agile") == 15, "kw: in qual"
assert compute_keyword_rating("cobol",    "Engineer", "Java Dev", "Python work", "Java skills") == 100, "kw: not found"
print("PASS  compute_keyword_rating")
 
# --- check_if_state_in_region ---
assert check_if_state_in_region(42, 15) == 0,   "state_in_region: Texas in Southwest"
assert check_if_state_in_region(42, 9)  == 100, "state_in_region: Texas not in Northeast"
print("PASS  check_if_state_in_region")
 
# --- check_if_city_in_region ---
assert check_if_city_in_region(6, 15) == 0,   "city_in_region: Austin in Southwest"
assert check_if_city_in_region(6, 9)  == 100, "city_in_region: Austin not in Northeast"
print("PASS  check_if_city_in_region")
 
# --- compute_region_rating ---
sw_idx   = find_region_index("southwest")
west_idx = find_region_index("west")
assert compute_region_rating(sw_idx,   "southwest", "",      "")       == 0,   "region: exact"
assert compute_region_rating(sw_idx,   "",          "texas", "")       == 0,   "region: texas state in southwest"
assert compute_region_rating(sw_idx,   "",          "",      "austin") == 0,   "region: austin city in southwest"
assert compute_region_rating(west_idx, "",          "maine", "")       == 100, "region: maine not in west"
print("PASS  compute_region_rating")
 
# --- compute_state_rating ---
tx_idx = find_state_index("texas")
assert compute_state_rating(tx_idx, "", "texas",    "")       == 0,   "state: exact"
assert compute_state_rating(tx_idx, "", "oklahoma", "")       == 30,  "state: oklahoma neighbor of texas"
assert compute_state_rating(tx_idx, "", "",         "austin") == 0,   "state: austin city -> texas"
assert compute_state_rating(tx_idx, "", "maine",    "")       == 100, "state: maine not near texas"
print("PASS  compute_state_rating")
 
# --- compute_city_rating ---
austin_idx = find_city_index("austin")
assert compute_city_rating(austin_idx, "austin")      == 0,   "city: exact"
assert compute_city_rating(austin_idx, "san antonio") == 20,  "city: san antonio neighbor of austin"
assert compute_city_rating(austin_idx, "boston")      == 100, "city: boston not near austin"
assert compute_city_rating(austin_idx, "")            == 100, "city: no city on job"
print("PASS  compute_city_rating")
 
# --- compute_job_rating master function ---
sample_job = {
    "JOB_TYPE":       "regular",
    "JOB_TITLE":      "Database Administrator",
    "SPECIALIZATION": "Database Administration",
    "REGION_NAME":    "",
    "STATE_NAME":     "texas",
    "LOCATION":       "austin",
    "MIN_SALARY":     70000,
    "MAX_SALARY":     90000,
    "COMPANY_NAME":   "IBM",
    "DESCRIPTION":    "Looking for Oracle DBA with Python skills.",
    "QUALIFICATION":  "5 years of database experience required.",
}
 
params_none = {
    "job_type": "", "location_type": "", "location_value": "",
    "min_salary": 0, "company_name": "", "keyword": ""
}
 
assert compute_job_rating(sample_job, params_none)                                    == 100, "master: no filters"
assert compute_job_rating(sample_job, {**params_none, "job_type": "regular"})         == 100, "master: exact job type"
assert compute_job_rating(sample_job, {**params_none, "job_type": "intern"})          <  100, "master: intern vs regular deducts"
assert compute_job_rating(sample_job, {**params_none, "keyword": "database"})         == 100, "master: keyword in title"
assert compute_job_rating(sample_job, {**params_none, "keyword": "cobol"})            ==   0, "master: keyword miss -> 0"
assert compute_job_rating(sample_job, {**params_none, "company_name": "IBM"})         == 100, "master: exact company"
assert compute_job_rating(sample_job, {**params_none, "company_name": "Intel"})       <  100, "master: similar company partial"
assert compute_job_rating(sample_job, {**params_none, "location_type": "state",
                                                      "location_value": "texas"})     == 100, "master: exact state"
assert compute_job_rating(sample_job, {**params_none, "min_salary": 70000})           == 100, "master: salary met"
assert compute_job_rating(sample_job, {**params_none, "min_salary": 150000})          <  100, "master: salary not met deducts"
print("PASS  compute_job_rating (master)")
 
print()
print("All tests passed.")