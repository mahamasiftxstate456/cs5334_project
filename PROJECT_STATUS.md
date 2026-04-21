# CS5334 - Job Search Project
## Python + Oracle Implementation

---

## Demo Files Structure
The professor provided a working demo in C++/Perl. These are reference files only — do not modify them.

```
demo_projectfiles/
├── c++/
│   ├── ematch_job.pc          # Main search logic (SQL query building)
│   ├── ematch_class.cxx       # Rating engine (region, state, city, salary)
│   ├── ematch_class.h         # Class definition
│   └── ematch_const_struct.h  # All location lookup tables (states, cities, regions)
│
├── cgi-bin/
│   ├── jobsearch.pl           # Main CGI handler (reference for jobsearch.py)
│   ├── getjob.pl              # Job detail page (reference for getjob.py)
│   ├── home.pl                # Homepage (already implemented as home.py)
│   └── common.cgi             # Shared utilities (already implemented as common.py)
│
└── html/
    └── job_search.html        # Search form (already implemented)
```

---

## Python Project Setup
All files go under `/home/netid/public_html/` on `newfirebird.cs.txstate.edu`

```
public_html/
├── html/
│   └── job_search.html        # DONE - search form
│
├── cgi-bin/
│   ├── __init__.py            # DONE - empty, makes cgi-bin a package
│   ├── common.py              # DONE - HTML header and footer
│   ├── home.py                # DONE - homepage with live DB counts
│   ├── jobsearch.py           # *** TO IMPLEMENT - see instructions inside ***
│   └── getjob.py              # *** TO IMPLEMENT - see instructions inside ***
│
└── lib/
    ├── __init__.py            # DONE - empty, makes lib a package
    ├── db.py                  # DONE - Oracle database connection
    ├── config.py              # DONE - all constants, penalties, similar companies
    ├── location_data.py       # DONE - all US region, state, city lookup tables
    └── rating.py              # *** TO IMPLEMENT - see instructions inside ***
```

---

## Files Already Done
| File | What it does |
|---|---|
| `lib/db.py` | Connects to Oracle using cx_Oracle |
| `lib/config.py` | Job type penalties, similar companies, salary ranges |
| `lib/location_data.py` | US regions, states, cities, neighbor ratings, region compatibility matrix |
| `cgi-bin/common.py` | HTML header and footer matching demo UI exactly |
| `cgi-bin/home.py` | Homepage showing live job and member counts from DB |
| `html/job_search.html` | Search form matching demo UI exactly |
| `lib/__init__.py` | Empty package marker |
| `cgi-bin/__init__.py` | Empty package marker |

---

## Three Files Left To Implement

### 1. `lib/rating.py`
**The rating engine. Most important file.**
Contains all functions that calculate how well a job matches the user's search.
Implements all 4 required project features.

> **Read the implementation guide comments at the top of the file.**
> They explain every function in detail with examples.

Depends on:
- `lib/config.py` for JOB_TYPE_PENALTY and SIMILAR_COMPANIES
- `lib/location_data.py` for all location lookup tables and helper functions

---

### 2. `cgi-bin/jobsearch.py`
**The main CGI handler. The core of the application.**
Called when user submits the search form. Fetches jobs from DB,
rates them, sorts them, paginates and displays results.

> **Read the implementation guide comments at the top of the file.**
> They explain every function in detail with step by step instructions.

Depends on:
- `lib/db.py` for database connection
- `lib/config.py` for salary lookup
- `lib/rating.py` for compute_job_rating()
- `cgi-bin/common.py` for print_header() and print_footer()

---

### 3. `cgi-bin/getjob.py`
**The job detail page.**
Shows full job details when user clicks a job title in results.
Improved version of demo's getjob.pl — actually queries DB
to show DESCRIPTION and QUALIFICATION which the demo never showed.

> **Read the implementation guide comments at the top of the file.**
> They explain every function in detail with step by step instructions.

Depends on:
- `lib/db.py` for database connection
- `cgi-bin/common.py` for print_header() and print_footer()

---

## Setup Instructions

### Install cx_Oracle on newfirebird
```bash
pip3 install cx_Oracle --user
```


### Test database connection
```bash
cd /home/netid/public_html
python3 lib/db.py
# Should print: SUCCESS - Connected to Oracle!
```

### Access the project
```
http://newfirebird.cs.txstate.edu/~netid/html/job_search.html
```

---

## Implementation Order
Implement files in this exact order — each one depends on the previous:

```
1. lib/rating.py       (no web, pure logic - test with python3 rating.py)
2. cgi-bin/jobsearch.py (test through browser after rating.py works)
3. cgi-bin/getjob.py   (test by clicking a job title in results)
```
