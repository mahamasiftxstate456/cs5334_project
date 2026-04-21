#!/usr/bin/perl
# This program takes the job id argument and fetch all info about
#   a job and displayed it back to screen
#  
#   Created:  01/20/2001
#   Modified: 03/31/2003
#   Modified: 02/21/2005
#             02/14/2012
#             
#             03/30/2017

require "common.cgi";


&get_parameters( *contents );

#&log("Display job by id $contents{id}"); 

print "Content-Type: text/html\n\n";

&print_header;

print "<h2> Job description</h2>\n";
print "<form action=\"/~wp01/cgi-bin/submit_resume.pl\">\n";

# Print the job information
$company=$contents{company};
$job_title=$contents{job_title};
$location=$contents{location};
$salary=$contents{salary};
$specialty=$contents{specialty};
print <<EOF;
<b>
Job Title: <font color="#006600"> $job_title </font> 
<br>
Specialized area:     <font color="#006600"> $specialty </font>
<br>
Location: <font color="#006600">  $location </font>
<br>
Company: <font color="#006600">  $company </font>
<br>
Salary: <font color="#006600">  $salary </font>
<br>
Job Description: 
</b>
<br>
$description
<br>
<br>
EOF
print "Copy and paste your text resume into the following window";
print " if interested.<br>\n";
print "<textarea rows=20 cols=60 name=resume>\n";
print "</textarea><br>\n";
print "<input type=submit value=\"Submit your resume for this job\">\n";
print "</form>\n";
&print_tailer;

