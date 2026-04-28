# CS5334 Project Submission Report
CS5334.251/R02 — Advanced Information Processing, Spring 2026
 
**Group Members:** Maham Asif, Natalie Leal Blanco
 
---
 
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
 
**Feature 2 — Company Name Rating**
 
The demo's original behavior placed `company_name` in the SQL `WHERE`
clause, returning only exact company matches. Our implementation removes
`company_name` from `WHERE`. All jobs are returned and each receives a penalty
based on company match quality. An exact company name match (case-insensitive)
receives no penalty. An unrelated company receives a penalty of 60, keeping it in
results but ranked near the bottom.
 
**Feature 3 — Similar Company Search**
 
Implemented as part of the company rating function. A lookup table
`SIMILAR_COMPANIES` in `lib/config.py` maps each company to a list of related
companies with associated penalties. When a user searches for a company such as
"Intel", jobs from similar companies such as "AMD" or "Nvidia" are returned with
a reduced penalty rather than the full unrelated penalty. This allows users to
discover relevant jobs at related employers without explicitly searching for each
one.
 
**Feature 4 — Keyword Search**
 
The keyword field existed in the demo's HTML form but was never
processed by the backend. Our implementation searches the keyword across four job
text fields in priority order: `JOB_TITLE` and `SPECIALIZATION` (no penalty if
found), `DESCRIPTION` (penalty 10 if found here first), and `QUALIFICATION`
(penalty 15 if found here first). If the keyword is not found in any field, the
job receives a penalty of 100 and is excluded from results. All comparisons are
case-insensitive substring searches.
 
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
handled by SQL and which were handled by `ematch_class.cxx`. In our
`jobsearch.py`, `build_sql_query()` places only `JOB_TITLE` and `SPECIALIZATION`
in `WHERE`, matching the demo's exact behavior for those two fields. All other
filtering goes through `compute_job_rating()`.
 
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
 
---
 
### README
 
See `README.md` in the source directory documented below. It includes the complete
URL, instructions for running the program, and setup steps.
 
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