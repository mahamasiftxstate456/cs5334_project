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

### Day 1 Objectives
- verify repo structure 
- separate reference vs implementation files
- prepare local workspae
- set up server environemnt 
- verify base demo runs

### Day 1 Server Setup Progress

- bashrc setup
    - Created `bashrc.txt` manually on `newfirebird` using the course file contents
    - Successfully sourced the file
    - Confirmed: 
        - `CLASSPATH` populated
        - `LD_LIBRARY_PATH` populated
        - `CATALINA_HOME` populated

### Day 1 Notes 

- Demo successfully deployed and running on newfirebird
- Backend pipeline confirmed working:
    HTML -> CGI -> C++ -> Oracle DB -> Results

#### Known Issues
- Top navigation buttons (Home, Job Search)do not function correctly
- Direct links and search functionality work as expected
- Issues likely due to outdated frame-based JavaScript targeting

#### Conclusion
- Core system functionality is verified
- Ready to proceed to code analysis and feature implementation