# CS5334 Job Search Project — README
CS5334.251/R02 — Advanced Information Processing, Spring 2026

---

## How to Access and Run the Program

This is a Python CGI application running on `newfirebird.cs.txstate.edu`.
There is no compilation step. The program runs through a browser.

**Open this URL in a browser:**

```
http://newfirebird.cs.txstate.edu/~[netid]/html/job_search.html
```

This loads the job search form. Fill in any combination of the search fields
and click Submit. Results appear ranked by match quality, highest first.
Click any job title in the results to view the full job detail page.

---

## Source File Location

All source files are on `newfirebird.cs.txstate.edu` at:

```
/home/[netid]/public_html/
    html/
        job_search.html       — search form
    cgi-bin/
        common.py             — shared HTML header and footer
        home.py               — homepage
        jobsearch.py          — main search handler (called when form is submitted)
        getjob.py             — job detail page (called when a job title is clicked)
    lib/
        db.py                 — Oracle database connection
        config.py             — job type penalties, similar companies, salary table
        location_data.py      — region, state, and city lookup tables
        rating.py             — rating engine implementing all four project features
    tests/
        test_rating.py        — tests for lib/rating.py
        test_getjob.py        — tests for cgi-bin/getjob.py
        test_jobsearch.py     — tests for cgi-bin/jobsearch.py
```

---

## Setup (for running on a new server)

**1. Fill in database credentials in `lib/db.py`:**

```python
DB_USER     = "your_netid"
DB_PASSWORD = "your_oracle_password"
DB_DSN      = "csdbora"
```

**2. Ensure Oracle environment variables are set.**

`lib/db.py` sets these automatically at runtime:

```python
os.environ["ORACLE_HOME"]     = "/usr/lib/oracle/21/client64"
os.environ["LD_LIBRARY_PATH"] = "/usr/lib/oracle/21/client64/lib"
os.environ["TNS_ADMIN"]       = "/usr/lib/oracle/21/client64/network/admin"
```

**3. Ensure `cx_Oracle` is installed:**

```bash
pip3 install cx_Oracle --user
```

**4. Set execute permissions on CGI scripts:**

```bash
chmod 755 ~/public_html/cgi-bin/*.py
```

**5. Verify the database connection:**

```bash
cd ~/public_html
python3 lib/db.py
```

Expected output: `SUCCESS - Connected to Oracle!`

---

## Running the Tests

```bash
cd ~/public_html
python3 tests/test_rating.py
python3 tests/test_getjob.py
python3 tests/test_jobsearch.py
```

All 37 tests should print PASS and exit cleanly.

---

## How the Rating System Works

Every job starts with a score of 100. Each rating function calculates a numeric
deduction. The master function subtracts deductions one at a time and stops
immediately if the score reaches 0. Higher score means better match and appears
higher in results. A score of 0 means the job is excluded entirely.

The four project features are implemented as rating functions in `lib/rating.py`:

- `compute_job_type_rating()` — penalizes job type mismatch (Feature 1)
- `compute_company_rating()` — penalizes company mismatch, rewards similar companies (Features 2 and 3)
- `compute_keyword_rating()` — penalizes missing keyword or keyword in a lower-priority field (Feature 4)

Location and salary rating functions are ported directly from the demo's
`ematch_class.cxx` and operate the same way as in the original program.

---

## Features Not Implemented

The following were not part of the four required project features and are
not implemented:

- Employer login and registration
- Member login and registration
- Resume submission backend — the submit button on the job detail page is
  present but not processed (`submit_resume.pl` was never provided in the demo)