# Feature Specs

## 1. System Architecture

### 1.1 Overview
The job search application follows a multi-layer architecture consisting of:
    - HTML frontend (user interface)
    - CGI layer (request handling)
    - Backend logic (Python implementation)
    - Oracle database (data storage)

The system processes user input from a web form, passes it through a CGI layer, executes search and ranking logic in the backend, and returns ranked job results to the user.

### 1.2 Layer Breakdown

#### HTML Lyer (Frontend)
Located in `html/`

- Contains pagres such as `index.html`, `title.html`, and `job_search.html`
- Provides the job search form for user input
- Sends search parameters (e.g., job type, company name, keyword) to the CGI layer

#### CGI Layer (Request Handling)
Located in: `cgi-bin/`

- Includes scripts such as `jobsearch.pl`, `home.pl`, and `common.cgi`
- Receives form input from HTML
- Converts input into a query string format (name=value pairs)
- Passes the query to the backend search logic

### Backend Layer (Python Implementation)
Located in: `python/`

- Responsible for query construction and job rating
- Implements the required features: 
    - job type rating
    - company name rating
    - similar company matching
    - keyword search
- Processes results and computes a final ranking score

#### Databse Layer (Oracle)
- Stores job-related data (job, employer, member tables)
- Queried by the backend logic
- Provides raw job records that are later ranked

### 1.3 Request Flow

1. The user opens `job_search.html` in the browser
2. The user submits the search form with selected parameters
3. The request is sent to `jobsearch.pl` in the CGI layer
4. The CGI script builds a query string containing all parameters
5. The backend Python logic receives and parses the parameters
6. A SQL query is constructured to retrieve relevant job records
7. Each job is evaluated using a rating function
8. Results are sorted by rating and returned to the user

### 1.4 Reference vs Implementation

The repository includes a reference implementation in `reference/demo_projectiles/`, which contains:
    - C++ (Proc*C) backend code
    - CGI scripts
    - HTML files

These files are used to understand:
    - how queries are constructed
    - how rating logic is applied
    - how data fields are structured

The actual implementation for this project is developed in Python, which mirrors the behavior of the reference system while extending it with new features.

### 1.5 Current System Behavior

In the reference implemantaion:
    - `job_type` is used as an exact match in the SQL WHERE clause
    - `company_name` is also used as an exact match in the WHERE clause

This means:
    - only jobs that exactly match these fields are returned
    - no partial matches or related results are shown

This limits the flexibility of the search system.

### 1.6 Target System Behavior

In the updated system:
    - `job_type` and `company_name` will be removed from the WHERE clause 
    - all jobs will be retrieved (subject to other filters)
    - ranking will be applied using a rating system

This allows:
    - partial matches to be included
    - similar job types and companies to appear
    - more flexible and realistic search results

### 1.7 Rating System Overview

Each job result is assigned a score based on how well it matched user input.

The base score starts at 100 and deductions are applied based on:
    - job tyoe mismatch
    - company mismatch
    - location mismatch (existing logic)
    - salary mismatch (existing logic)
    - keyword relevance (new feature)

Final score:
    final_rating = 100 - total_deductions

Jobs with higher scores appear first in results. Jobs with very low or zero scores may be excluded.

## 2. Feature 1: Job Type Rating
## 3. Feature 2:  Compnay Name Rating
## 4. Feature 3: Similar Company Search
## 5. Feature 4: Keyword Search