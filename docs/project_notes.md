# Project Notes

## Goal
Extend the Python flavor of the job search demo with:
    1. Job Type Rating
    2. Company Name Rating
    3. Similar Company Searc
    4. Keyboard Search

## Current Repo State
- README file exists
- demo_projectfiles contains c++, cgi-bin, html
- no branched yet
- ptyhon implementation files not yet added

## Natalie 

### Objectives
- verify repo structure 
- separate reference vs implementation files
- prepare local workspace (Cursor)
- set up server environemnt (newfirebird)
- deploy and verify base demo system
- Understand full system architecture and data flow

### Server Setup Progress

- bashrc setup
    - Created `bashrc.txt` manually on `newfirebird` using the course file contents
    - Successfully sourced the file
    - Confirmed: 
        - `CLASSPATH` populated
        - `LD_LIBRARY_PATH` populated
        - `CATALINA_HOME` populated

### Database Setup

- Imported `expdat.dmp` into Oracle (`csdbora`)
- Import completed successfully (with expected warning due to duplicate keys)
- Verified:
    - Tables exist
    - Data is populated
- Confirmed databse connectivity through backend execution

### Demo Deployment

- Installed required demo files:
  - `proc-demo.tar`
  - `cgi-bin.tar`
- Established directory structure under `~/public_html`
- Configured system paths:
  - Replaced `/~wp01/` → `/~vya16/` (HTML)
  - Replaced `/home/wp01/` → `/home/vya16/` (CGI)
- Compiled backend executables:
  - `ematch_job`
  - `real_time_number`
- Moved executables into `cgi-bin`
- Set correct execution permissions

### Deployment Result

- Demo successfully deployed and accessible via browser
- Core system pipeline verified:

```text
User → HTML → CGI (Perl) → C++ → Oracle DB → Results → Browser

#### Known Issues
- Top navigation buttons (Home, Job Search)do not function correctly
- Direct links and search functionality work as expected
- Issues likely due to outdated frame-based JavaScript targeting

### Conclusion

- The system has been successfully deployed and verified end-to-end  
- Data flow across all layers is fully understood  
- Responsibilities of each component are clearly identified  
- Key modification points for feature implementation have been mapped  
- The project is ready to transition into feature development

## Maham

### Python Implementation

- Created core modules inside `python/`
- Implemented system logic previously absent
- Established a clear structure for: 
  - Execution flow
  - Data handling
  - Funcitonal components

Design focus:
- Modularity
- Readability
- Exentibility

## Natalie 

- Implemented rating.py. 

  -> Implemented all rating and penalty functions for the job search engione. Every job starts with a base score of 100. Each function returns a deduction that is subtracted from that base. Jobs that reach 0 or below are excluded from results. The following functions were implemented:
  
  **Location helpers (ported from demo's ematch_class.cxx):**
  - `check_if_state_in_region(state_index, region_index)` - binary check returning 0 or 100
  - `check_if_city_in_region(city_index, region_index)` - fallback when job hs no region or state
  - `compute_salary_rating(asked_min_salary, job_min_salary)` - proportional penalty using demo's formula
  - `compute_region_rating(...)` - 3-case logic using REGION_COMPATIBILITY matrix
  - `compute_state_rating(...)` - walks NEIGHBOR_STATE_RATINGS with city and region fallbacks
  - `compute_city_rating(..) - exact match first, then walks NEIGHBOR_CITY_RATINGS

  **Project Features:**
  - `compute_job_type_rating()` - Feature 1: replaces the demo's exact WHERE clause filter with a penalty table from JOB_TYPE_PENALTY in config.py, so all job types are returned and ranked.
  - `compute_company_rating()` - Features 2 & 3: replaces exact company filter with a rating system; similar companies are returned with a reduced penalty using SIMILAR COMPANIES in config.py.
  - `compute_keyword_rating()` - Feature 4: implements the keyword field that existed in the demo HTML form but was never processed by the backend; searched JOB_TITLE, SPECIALIZATION, DESCRIPTION, and QUALIFICATION in priority order with tiered penalties (0/10/15/100).
  -   compute_job_rating()` - master function that applies all deductions in order with early exit when score reaches 0.
- Created tests folder
  - Created test_rating.py
      - Standalone test file for rating.py. Covers every implemented function with multiple cases including edge cases, exact matches partial matched, and exclusion cases. 