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

## Natalie Day 1 - Apr 20 

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