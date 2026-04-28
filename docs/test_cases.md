# Test Cases
 
---
 
## Basic Functionality
 
1. Submit with all fields set to "All" / "Any" / no keyword — should return all jobs, all rated 100
2. Submit with just a job title selected — should return only jobs matching that title
3. Submit with just a specialization selected — should return only jobs matching that specialization
---
 
## Feature 1 — Job Type Rating
 
4. Select "regular" job type, all else "All" — regular jobs should score 100, other types should appear below with lower scores
5. Select "intern" job type — intern jobs score 100, co-op jobs should appear close behind, regular jobs ranked lower
6. Confirm no job type is completely excluded — every type should still appear, just ranked differently
---
 
## Feature 2 — Company Name Rating
 
7. Select "Intel" as company, all else "All" — Intel jobs should score 100 and appear first
8. Select a company with no jobs in the database — results should still appear, just all with the unrelated penalty of 60 or lower
---
 
## Feature 3 — Similar Company Search
 
9. Select "Intel" as company — AMD, Nvidia, and other similar companies should appear in results with a score between 0 and 100, ranked below Intel but above unrelated companies
10. Confirm the order: Intel jobs first, then similar companies, then unrelated companies at the bottom
---
 
## Feature 4 — Keyword Search
 
11. Enter a keyword that appears in a job title (e.g. "engineer") — those jobs should score 100
12. Enter a keyword that appears only in description — those jobs should appear but scored lower than title matches
13. Enter a keyword that appears only in qualification — should appear but ranked below description matches
14. Enter a keyword that exists nowhere (e.g. "blockchain") — those jobs should be completely excluded from results
15. Enter a keyword in mixed case (e.g. "DATABASE") — should match "database" in any field, confirming case-insensitivity
---
 
## Location Rating
 
16. Select a specific region — jobs in that region score highest, neighboring regions appear with a penalty
17. Select a specific state — jobs in that state score highest, neighboring states appear below
18. Select a specific city — jobs in that city score 100, neighboring cities appear with a penalty, distant cities excluded
---
 
## Salary Rating
 
19. Select a high salary (e.g. "15-up") — jobs meeting that salary score 100, jobs below it are penalized proportionally
20. Select "Any" salary — no salary deduction applied, all jobs unaffected by salary
---
 
## Pagination
 
21. Run a broad search that returns more than 16 results — confirm Next Page and Previous Page links appear and work
22. Click through to page 2 and confirm the job numbers continue from 17 onward
---
 
## Job Detail Page
 
23. Click any job title in results — confirm the detail page loads with title, type, company, location, salary, description, and qualification all populated
24. Click a job where description or qualification may be empty — confirm the fallback messages ("No description available") appear instead of a blank
---
 
## Combined Filters
 
25. Select a job type + keyword together — confirm both penalties apply and ranking reflects both
26. Select a company + location together — confirm results reflect both deductions stacked
27. Select filters that together produce zero results — confirm the page shows "0 matches" gracefully rather than crashing