#!/usr/bin/env python3
"""
cgi-bin/common.py
-----------------
Shared HTML header and footer functions used by ALL other CGI scripts.
Matches the professor's original demo UI exactly:
  - Blue title bar (#3366ff)
  - Cyan nav buttons (#ccffff)
  - White results background (#FFFFFF)

Folder: cgi-bin/common.py

Usage (from another CGI file):
    from common import print_header, print_footer
    print_header("Job Search Results")
    # ... your page content here ...
    print_footer()
"""


def print_header(page_title="DrPengsAIIPDemos Job Search"):
    """
    Prints the HTML header for every page.

    Outputs:
      - HTTP Content-Type line (required by web server)
      - Opening <html>, <head>, <body> tags
      - Blue title bar with site name (matches professor's demo)
      - Cyan navigation button bar

    Parameters:
        page_title (str) -- the title shown on the browser tab
    """

    # MUST come first - tells the web server this is HTML
    print("Content-Type: text/html")
    print()  # blank line required after Content-Type

    # Opening tags - white background like the results page in the demo
    print(f"""<html>
<head>
<title>{page_title}</title>
</head>
<body BGCOLOR="#FFFFFF" LINK="#0088ff" ALINK="#FF0000" VLINK="#CC0000">
""")

    # Blue title bar - exactly like title.html in the demo
    print("""
<table width="800" bgcolor="#3366ff">
<tr>
    <td>
        <H1><i><font color="#ffcc00"> DrPengsAIIPDemos.Com </font></i></H1>
    </td>
</tr>
<tr>
    <td>
        <font color="#ffffcc">The on-line career and recruitment center
        dedicated to the high tech industry over the world</font>
    </td>
</tr>
</table>
""")

    # Cyan navigation button bar - matches the demo buttons exactly
    print("""
<TABLE CELLSPACING="0" CELLPADDING="3" BORDER="0">
<tr>
    <td><a href="/~netid/cgi-bin/home.py">Home</a></td>
    <td><a href="/~netid/html/job_search.html">Job Search</a></td>
</tr>
</TABLE>
<br>
""")


def print_footer():
    """
    Prints the HTML footer for every page.

    Outputs:
      - Bottom navigation links (same as demo's print_tailer)
      - Copyright line
      - Closing </body> and </html> tags
    """

    print("""
<br><br>
<center>
<TABLE CELLSPACING="0" CELLPADDING="3" BORDER="0">
<tr>
    <td><a href="/~netid/cgi-bin/home.py">Home</a></td>
    <td><a href="/~netid/html/job_search.html">Job Search</a></td>
</tr>
</table>
<br>
<i>Copyright &copy; 2026 DrPengsAIIPDemos.com Inc. All rights reserved.</i>
</center>
</body>
</html>
""")


# -----------------------------------------------
# ONLY runs when you do: python3 common.py
# IGNORED when another file imports this file
# -----------------------------------------------
if __name__ == "__main__":
    print_header("Test Page")
    print("<center><h2>Hello! This is the page content area.</h2></center>")
    print_footer()