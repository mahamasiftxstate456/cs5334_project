# CS5334 Project Submission Report
CS5334.251/R02 — Advanced Information Processing, Spring 2026

**Group Members:** Maham Asif, Natalie Leal Blanco

## Project Description

### Features Implemented

**Feature 1 — Job Type Rating**

The demo's original behavior placed `job_type` in the SQL `WHERE`
clause, returning only jobs with an exact type match. Our implementation removes
`job_type` from `WHERE` entirely. All jobs are returned from the database, and each
is assigned a numeric penalty based on how far its type is from what the user
requested. An exact match receives no penalty. Related types receive a smaller
penalty. Distant types receive a larger penalty. Jobs are not excluded based on
type alone — they rank lower. The penalty values are defined in a 2D lookup table
`JOB_TYPE_PENALTY` in `lib/config.py`. If a job type is not represented in the
table, a default penalty of 30 is applied.

Special technique used:
A two-dimensional dictionary `JOB_TYPE_PENALTY` in `lib/config.py` stores all
penalty values indexed as `JOB_TYPE_PENALTY[asked_type][job_type]`. This mirrors
the same neighbor-table approach the demo uses for location rating in
`ematch_const_struct.h`.

**Feature 2 — Company Name Rating**

The demo's original behavior placed `company_name` in the SQL `WHERE`
clause, returning only exact company matches. Our implementation removes
`company_name` from `WHERE`. All jobs are returned and each receives a penalty
based on company match quality. An exact company name match (case-insensitive)
receives no penalty. An unrelated company receives a penalty of 60, keeping it in
results but ranked near the bottom.

Special technique used:
Company matching uses case-insensitive string comparison to handle minor
differences in capitalization between form input and database values. The function
first tries the original string as a key, then scans all `SIMILAR_COMPANIES` keys
case-insensitively as a fallback.

**Feature 3 — Similar Company Search**

Implemented as part of the company rating function. A lookup table
`SIMILAR_COMPANIES` in `lib/config.py` maps each company to a list of related
companies with associated penalties. When a user searches for a company such as
"Intel", jobs from similar companies such as "AMD" or "National Semiconductor" are
returned with a reduced penalty rather than the full unrelated penalty. This allows
users to discover relevant jobs at related employers without explicitly searching
for each one.

Special technique used:
The `SIMILAR_COMPANIES` dictionary was designed to mirror the same structure as the
demo's neighbor state and city rating tables. Each company maps to a list of
`(similar_company, penalty)` tuples, exactly as each state maps to a list of
`(neighbor_state, penalty)` pairs in the demo's `ematch_const_struct.h`.

**Feature 4 — Keyword Search**

The keyword field existed in the demo's HTML form but was never processed by the
backend. Our implementation searches the keyword across four job text fields in
priority order: `JOB_TITLE` and `SPECIALIZATION` (no penalty if found),
`DESCRIPTION` (penalty 10 if found here first), and `QUALIFICATION` (penalty 15 if
found here first). If the keyword is not found in any field, the job receives a
penalty of 100 and is excluded from results. All comparisons are case-insensitive
substring searches.

Special technique used:
The keyword search uses a priority-ordered field search rather than a simple
found/not-found check. Finding the keyword in the job title signals a stronger
match than finding it only in the qualifications list. The tiered penalties
(0, 10, 15, 100) produce finer-grained ranking across keyword results. The keyword
is searched across both the job table fields (JOB_TITLE, SPECIALIZATION) and the
job description text (DESCRIPTION, QUALIFICATION), satisfying the project
requirement of searching both the job table and the job description.

---

### Features NOT Implemented

The following features were not part of the four project requirements and were not
implemented:

- Employer login and registration pages (`employer_login.html` backend)
- Member login and registration pages (`member_login.html` backend)
- Resume submission backend — the submit button on the job detail page points to
  `submit_resume.pl` which was never provided in the demo and is not implemented
- Member-based automatic resume matching and email notification service

These features were not listed in the project requirements and are noted here for
completeness.

---

### How the System Works

The application follows the same multi-layer architecture as the class demo:

```
User → job_search.html → jobsearch.py (CGI) → Oracle DB → rating engine → results
```

**Step 1 — User submits the search form**

The user opens `job_search.html` and selects search criteria including job type,
job title, specialization, location (region/state/city), salary, company, and an
optional keyword. Clicking "Go Search!" sends all parameters to `jobsearch.py` as
a GET request.

**Step 2 — CGI script parses form input**

`jobsearch.py` reads all form parameters using `cgi.FieldStorage()`. It converts
the salary form code (e.g. "7-10") to an actual number (70000) and determines
which location dropdown the user selected based on the radio button value.

**Step 3 — SQL query is built**

`build_sql_query()` in `jobsearch.py` constructs the SQL query. Only `JOB_TITLE`
and `SPECIALIZATION` go into the SQL `WHERE` clause as exact match conditions,
matching the demo's behavior for those two fields. Job type, company, location,
salary, and keyword are intentionally excluded from SQL and handled by the rating
system instead. This is the key structural difference from the demo.

**Step 4 — All matching rows are fetched from Oracle**

`fetch_all_job_rows()` executes the SQL against the Oracle database on
`oracle.cs.txstate.edu` using `cx_Oracle`. Each database row is converted from a
plain tuple into a named dictionary so column values can be accessed by name
(e.g. `job_row["COMPANY_NAME"]`) throughout the rating system.

**Step 5 — Every job row is rated**

`rate_and_sort_jobs()` calls `compute_job_rating()` from `lib/rating.py` once for
every job row returned from the database. The rating function starts every job at
100 and subtracts deductions in this order:

1. Job type penalty (Feature 1) — based on `JOB_TYPE_PENALTY` table
2. Location penalty — region, state, or city using neighbor tables ported from the
   demo's `ematch_const_struct.h`
3. Salary penalty — proportional formula ported exactly from `ematch_class.cxx`
4. Company penalty (Features 2 and 3) — exact match, similar companies, or
   unrelated using `SIMILAR_COMPANIES` table
5. Keyword penalty (Feature 4) — tiered search across four text fields

If the rating reaches 0 or below at any point the job is immediately excluded and
no further functions are called. This matches the demo's early-exit behavior.

**Step 6 — Results are sorted and paginated**

Jobs that survive rating are sorted highest rating first. Results are paginated at
16 per page, the same page size as the demo. Pagination links preserve the original
search parameters in the URL so filters are not lost when navigating between pages.

**Step 7 — HTML results table is printed**

The results table displays Job Number, Rating, Job Title (clickable link),
Special field, Location, Company, and Salary Range — the same seven columns as the
demo. The yellow row color `#FFFFCC` and overall page layout match the demo's UI.

**Step 8 — Job detail page**

Clicking a job title opens `getjob.py` which queries the database using the job ID
from the URL. This is an improvement over the demo's `getjob.pl` which only read
URL parameters and never queried the database, meaning `DESCRIPTION` was always
blank in the demo. Our version fetches and displays the full job row including
`DESCRIPTION` and `QUALIFICATION`.

---

### Special Techniques Used

**Rating system — deduction model ported from the demo**

The rating architecture directly follows the demo's `ematch_class.cxx`. Every job
starts at 100. Each rating function returns a numeric deduction. The master
function `compute_job_rating()` in `lib/rating.py` subtracts each deduction in
order. If the running total reaches 0 at any point, the job is immediately excluded
without evaluating remaining functions. This matches the demo's early-exit behavior.

**Removing job_type and company_name from SQL, moving them into rating**

The most significant structural change from the demo is that `job_type` and
`company_name` are removed from the SQL `WHERE` clause and handled entirely through
the rating system. This required understanding which fields in `ematch_job.pc` were
handled by SQL and which were handled by `ematch_class.cxx`. In our `jobsearch.py`,
`build_sql_query()` places only `JOB_TITLE` and `SPECIALIZATION` in `WHERE`,
matching the demo's exact behavior for those two fields. All other filtering goes
through `compute_job_rating()`.

**Location rating tables ported from demo**

All location lookup tables from the demo's `ematch_const_struct.h` were ported to
Python in `lib/location_data.py`. This includes the 17x17 region compatibility
matrix, neighbor state rating lists for all 50 states, neighbor city rating lists,
and the states-in-regions mapping. The rating logic from `ematch_class.cxx` for
region, state, and city rating was ported to `lib/rating.py` including the same
three-case fallback logic (region → state → city).

**Tiered keyword matching**

The keyword search uses a priority-ordered field search rather than a simple
found/not-found check. Finding the keyword in the job title signals a stronger
match than finding it only in the qualifications list. The tiered penalties
(0, 10, 15, 100) produce finer-grained ranking across keyword results.

**Case-insensitive company matching with fallback key scan**

`compute_company_rating()` performs a case-insensitive exact match first, then
looks up the company in `SIMILAR_COMPANIES`. Because table keys use the company's
canonical name, the function first tries the original string, then scans all keys
case-insensitively as a fallback. This handles user input variations without
requiring exact capitalization.

**Improved job detail page**

The demo's `getjob.pl` read job details from URL parameters only and never queried
the database. The `DESCRIPTION` field was referenced in the output code but never
assigned, so job descriptions were always blank. Our `getjob.py` queries the
database using the `job_id` from the URL with `WHERE JOB_ID = :job_id` and fetches
the complete job row including `DESCRIPTION` and `QUALIFICATION`, which are both
displayed on the detail page.

**Parameterized queries**

All database queries use Oracle bind variables (`:placeholder` syntax) rather than
string interpolation, preventing SQL injection and matching the approach in the
demo's Pro*C source.

**Import fix for CGI scripts**

Python cannot import from folders with a dash in the name. Since the folder is
named `cgi-bin`, the scripts add the `cgi-bin` folder to `sys.path` using
`sys.path.insert(0, os.path.dirname(__file__))` and then import with
`from common import print_header` rather than `from cgi-bin.common import`.

**No database tables were modified**

As noted in the project requirements, no tables in the Oracle database were
modified. All four new features are implemented entirely in the Python application
layer using the existing job table schema.

---

### README

#### Requirements

- Python 3 (available on newfirebird)
- cx_Oracle library: `pip3 install cx_Oracle --user`
- Oracle client libraries (already installed at `/usr/lib/oracle/21/client64`)
- Oracle database accessible at `oracle.cs.txstate.edu:1521`

#### Setup on newfirebird

1. Copy all project files to `/home/[netid]/public_html/`
2. Make CGI scripts executable:
```
chmod +x ~/public_html/cgi-bin/home.py
chmod +x ~/public_html/cgi-bin/jobsearch.py
chmod +x ~/public_html/cgi-bin/getjob.py
```
3. Fill in Oracle credentials in `lib/db.py`:
```
DB_USER     = "your_username"
DB_PASSWORD = "your_password"
DB_DSN      = "csdbora"
```
4. Test database connection:
```
cd ~/public_html
python3 lib/db.py
```
Should print: `SUCCESS - Connected to Oracle!`

#### Access the project

```
http://newfirebird.cs.txstate.edu/~[netid]/html/job_search.html
```

---

### Project URL

```
http://newfirebird.cs.txstate.edu/~[netid]/html/job_search.html
```

---

### Source Program Location

All source files are on `newfirebird.cs.txstate.edu` under:

```
/home/[netid]/public_html/
    html/
        job_search.html
    cgi-bin/
        common.py
        home.py
        jobsearch.py
        getjob.py
    lib/
        db.py
        config.py
        location_data.py
        rating.py
```

All functions are commented with their parameters, purpose, and return values.
Key design decisions are documented inline, including why `job_type` and
`company_name` are excluded from the SQL `WHERE` clause.