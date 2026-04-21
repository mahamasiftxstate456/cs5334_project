#!/usr/bin/env python3
"""
lib/config.py
-------------
All constant DATA for the job search project.
No logic, no database, no functions - just fixed data.

Matches EXACTLY what is in:
  - job_search.html  (dropdown options)
  - ematch_const_struct.h (job type, company data)
  - project description (4 new features)

Folder: lib/config.py

Usage:
    from lib.config import JOB_TYPES, JOB_TYPE_PENALTY, COMPANIES, SIMILAR_COMPANIES
"""


# -----------------------------------------------
# JOB TYPES
# Matches job_search.html dropdown exactly
# Also matches values stored in JOB_TYPE column
# -----------------------------------------------
JOB_TYPES = [
    "All",
    "regular",
    "entry_level",
    "intern",
    "co-op",
]


# -----------------------------------------------
# JOB TYPE RATING PENALTIES  (PROJECT FEATURE 1)
# -----------------------------------------------
# The demo currently uses job_type as a WHERE clause
# (exact match only). The project asks us to change
# this to a RATING system instead.
#
# Rule: start at 100, subtract penalty.
# If user picks "All" -> no penalty applied to anyone.
#
# How to read this table:
#   JOB_TYPE_PENALTY[what_user_asked][what_job_has]
#   = how much to deduct from rating
#
# Design rationale (matching demo's approach for location):
#   - Exact match          -> 0   penalty (100% rating)
#   - Very similar type    -> 20  penalty (80%  rating)
#   - Somewhat related     -> 30  penalty (70%  rating)
#   - Not really related   -> 50  penalty (50%  rating)
# -----------------------------------------------
JOB_TYPE_PENALTY = {
    "regular": {
        "regular":     0,    # exact match
        "entry_level": 20,   # close - regular is next step up from entry
        "intern":      40,   # not really what they want
        "co-op":       40,   # not really what they want
    },
    "entry_level": {
        "entry_level": 0,    # exact match
        "regular":     20,   # close - one step above entry level
        "intern":      30,   # somewhat related - both are junior roles
        "co-op":       30,   # somewhat related - both are junior roles
    },
    "intern": {
        "intern":      0,    # exact match
        "co-op":       10,   # very similar - both are temporary/student roles
        "entry_level": 30,   # somewhat related
        "regular":     50,   # not what they want at all
    },
    "co-op": {
        "co-op":       0,    # exact match
        "intern":      10,   # very similar - both are temporary/student roles
        "entry_level": 30,   # somewhat related
        "regular":     50,   # not what they want at all
    },
}


# -----------------------------------------------
# JOB TITLES
# Matches job_search.html dropdown exactly
# Used as WHERE clause (exact match) - NOT changed
# -----------------------------------------------
JOB_TITLES = [
    "All",
    "Analyst",
    "Senior Analyst",
    "Entry Level Engineer",
    "Engineer",
    "Senior Engineer",
    "Programmer Analyst",
    "Senior Programmer Analyst",
    "Staff Engineer",
    "Senior Staff Engineer",
    "Member of Technical Staff",
    "Senior Member of Technical Staff",
    "Production Operator",
    "Production Technician",
    "Supervisor",
    "Manager",
    "Project Manager",
    "Senior Manager",
    "Director",
    "Vice President",
    "Executive Vice President",
    "COO",
    "CFO",
    "CTO",
    "CEO",
]


# -----------------------------------------------
# SPECIALIZATIONS
# Matches job_search.html dropdown exactly
# Used as WHERE clause (exact match) - NOT changed
# -----------------------------------------------
SPECIALIZATIONS = [
    "All",
    "Accounting",
    "Analog Design",
    "Client Server Application Development",
    "Database Administration",
    "Database Development",
    "Device Driver Development",
    "Digital Design",
    "District Sales",
    "E-Commerce Development",
    "Embedded Software Development",
    "Embedded System",
    "Engineering",
    "Equipment",
    "Field Application",
    "Field Service",
    "Java Development",
    "Logic Design",
    "Mac Development",
    "Manufacturing",
    "Marketing",
    "MS Access Development",
    "Multimedia Application Development",
    "Network Security",
    "Operation",
    "Oracle DBA",
    "Oracle Development",
    "Process",
    "Process Integration",
    "Product",
    "Product Development",
    "Production",
    "Project Management",
    "Quality Control",
    "R&D",
    "Reliability",
    "Sales",
    "Signal Integrity",
    "Strategic Marketing",
    "System",
    "System Administration",
    "System Design",
    "System Integration",
    "System Quality Control",
    "System Testing",
    "Technical Support",
    "UNIX Administration",
    "UNIX System Programming",
    "Visual Basic Development",
    "VLSI Design",
    "Web Application Development",
    "Web Development",
    "Windows Administration",
    "Other",
]


# -----------------------------------------------
# COMPANIES
# Matches job_search.html dropdown exactly
# -----------------------------------------------
COMPANIES = [
    "All",
    "Apple Computers",
    "AMD",
    "Cirrus Logic",
    "Compaq",
    "Computer Associates",
    "CSC",
    "Dell",
    "EDS",
    "GE",
    "GMC",
    "Hewlett Packard",
    "IBM",
    "Intel",
    "Motorola",
    "National Semiconductor",
    "NEC",
    "Oracle",
    "SUN Microsystems",
    "Texas Instrument",
    "USDA",
]


# -----------------------------------------------
# SIMILAR COMPANIES  (PROJECT FEATURE 2 & 3)
# -----------------------------------------------
# Feature 2: company used as RATING (not WHERE clause)
#   - Exact match company -> 0 penalty (100% rating)
#   - All other companies -> apply penalty from below
#
# Feature 3: also return jobs from SIMILAR companies
#   - If user searches "IBM", also return Dell, HP jobs
#     with a rating penalty
#
# Structure:
#   SIMILAR_COMPANIES[searched_company] =
#       list of (similar_company, penalty)
#
# Penalty design:
#   - Direct competitor in same space -> 15-20 penalty
#   - Related but different space     -> 25-30 penalty
#   - Loosely related                 -> 35-40 penalty
# -----------------------------------------------
SIMILAR_COMPANIES = {
    "IBM": [
        ("Dell",                 20),
        ("Hewlett Packard",      20),
        ("Computer Associates",  25),
        ("CSC",                  30),
        ("EDS",                  30),
        ("NEC",                  35),
    ],
    "Intel": [
        ("AMD",                  15),
        ("National Semiconductor", 20),
        ("Cirrus Logic",         25),
        ("Texas Instrument",     25),
        ("NEC",                  30),
        ("Motorola",             30),
    ],
    "Apple Computers": [
        ("Dell",                 20),
        ("Hewlett Packard",      20),
        ("Compaq",               25),
        ("IBM",                  30),
    ],
    "Motorola": [
        ("Texas Instrument",     15),
        ("NEC",                  20),
        ("National Semiconductor", 20),
        ("Intel",                25),
        ("AMD",                  30),
    ],
    "Dell": [
        ("Compaq",               15),
        ("Hewlett Packard",      15),
        ("IBM",                  20),
        ("Apple Computers",      25),
        ("NEC",                  35),
    ],
    "Hewlett Packard": [
        ("Dell",                 15),
        ("Compaq",               15),
        ("IBM",                  20),
        ("Apple Computers",      25),
    ],
    "Oracle": [
        ("Computer Associates",  20),
        ("IBM",                  25),
        ("EDS",                  30),
    ],
    "SUN Microsystems": [
        ("Hewlett Packard",      20),
        ("IBM",                  25),
        ("Dell",                 30),
    ],
    "AMD": [
        ("Intel",                15),
        ("National Semiconductor", 20),
        ("Texas Instrument",     25),
        ("Cirrus Logic",         25),
        ("Motorola",             30),
    ],
    "Texas Instrument": [
        ("Motorola",             15),
        ("National Semiconductor", 20),
        ("Intel",                25),
        ("AMD",                  25),
        ("Cirrus Logic",         30),
    ],
    "Compaq": [
        ("Dell",                 15),
        ("Hewlett Packard",      15),
        ("IBM",                  20),
        ("Apple Computers",      30),
    ],
    "NEC": [
        ("IBM",                  20),
        ("Motorola",             25),
        ("Intel",                30),
    ],
    "National Semiconductor": [
        ("Intel",                20),
        ("AMD",                  20),
        ("Texas Instrument",     20),
        ("Cirrus Logic",         25),
        ("Motorola",             30),
    ],
    "Cirrus Logic": [
        ("National Semiconductor", 20),
        ("AMD",                  25),
        ("Texas Instrument",     25),
        ("Intel",                30),
    ],
    "Computer Associates": [
        ("Oracle",               20),
        ("IBM",                  25),
        ("EDS",                  30),
        ("CSC",                  30),
    ],
    "EDS": [
        ("CSC",                  20),
        ("IBM",                  25),
        ("Computer Associates",  30),
    ],
    "CSC": [
        ("EDS",                  20),
        ("IBM",                  25),
        ("Computer Associates",  30),
    ],
    "GE": [
        ("GMC",                  25),
        ("IBM",                  35),
    ],
    "GMC": [
        ("GE",                   25),
    ],
    "USDA": [],
}


# -----------------------------------------------
# SALARY RANGES
# Matches job_search.html dropdown exactly
#
# Each entry: (form_value, display_label, min_salary_number)
#   form_value        = what the HTML form sends
#   display_label     = what user sees in dropdown
#   min_salary_number = actual number for SQL/rating
# -----------------------------------------------
SALARY_RANGES = [
    ("Any",   "Any",           0),
    ("2-3",   "$20k - $30k",   20000),
    ("3-5",   "$30k - $50k",   30000),
    ("5-7",   "$50k - $70k",   50000),
    ("7-10",  "$70k - $100k",  70000),
    ("10-12", "$100k - $120k", 100000),
    ("12-15", "$120k - $150k", 120000),
    ("15-up", "$150k and up",  150000),
]

# -----------------------------------------------
# SALARY VALUE TO MIN LOOKUP
# Maps form_value -> min_salary_number
# Written out fully so it is easy to read and edit
# Used in rating.py to look up salary from form input
# -----------------------------------------------
SALARY_VALUE_TO_MIN = {
    "Any":   0,
    "2-3":   20000,
    "3-5":   30000,
    "5-7":   50000,
    "7-10":  70000,
    "10-12": 100000,
    "12-15": 120000,
    "15-up": 150000,
}


# -----------------------------------------------
# SALARY RATING FORMULA  (ported from demo)
# -----------------------------------------------
# From ematch_class.cxx compute_sal_rating():
#
#   if asked_min_salary > job_min_salary:
#       percent   = (asked_min_salary - job_min_salary) / asked_min_salary
#       deduction = percent * 100
#   else:
#       deduction = 0  (job pays enough or more, no penalty)
#
# This is NOT a lookup table - it is a formula.
# It lives in rating.py, documented here for reference.
# -----------------------------------------------


# -----------------------------------------------
# REGIONS
# Matches job_search.html dropdown exactly
# -----------------------------------------------
REGIONS = [
    "All",
    "Atlantic Coast",
    "East",
    "Great Lakes",
    "Middle",
    "Middle-west",
    "Mountain",
    "North",
    "Northeast",
    "Northwest",
    "Pacific Coast",
    "Pacific West",
    "South",
    "Southeast",
    "Southwest",
    "West",
]


# -----------------------------------------------
# ONLY runs when you do: python3 config.py
# IGNORED when another file imports this
# -----------------------------------------------
if __name__ == "__main__":
    print(f"Job Types        : {len(JOB_TYPES)} types")
    print(f"Job Titles       : {len(JOB_TITLES)} titles")
    print(f"Specializations  : {len(SPECIALIZATIONS)} fields")
    print(f"Companies        : {len(COMPANIES)} companies")
    print(f"Similar Groups   : {len(SIMILAR_COMPANIES)} groups")
    print(f"Salary Ranges    : {len(SALARY_RANGES)} ranges")
    print(f"Regions          : {len(REGIONS)} regions")

    print("\n--- JOB TYPE PENALTIES (sample) ---")
    print("User asks 'regular', job is 'intern' ->",
          JOB_TYPE_PENALTY["regular"]["intern"], "penalty =>",
          100 - JOB_TYPE_PENALTY["regular"]["intern"], "% rating")

    print("\n--- SIMILAR COMPANIES (sample) ---")
    print("Companies similar to Intel:")
    for company, penalty in SIMILAR_COMPANIES["Intel"]:
        print(f"  {company:30s} -> penalty={penalty}, rating={100-penalty}%")

    print("\n--- SALARY FORMULA (sample) ---")
    asked = 80000
    job   = 60000
    if asked > job:
        deduction = int(((asked - job) / asked) * 100)
        print(f"User wants ${asked:,}, job pays ${job:,} -> deduction={deduction}, rating={100-deduction}%")