#!/usr/bin/env python3
"""
cgi-bin/common.py
-----------------
Shared HTML header and footer functions used by ALL other CGI scripts.
Matches the professor's original demo UI exactly:
  - Blue title bar (#3366ff)
  - White results background (#FFFFFF)

Folder: cgi-bin/common.py

IMPORTANT:
  Content-Type: text/html is NOT printed here.
  Each file that uses print_header() must print Content-Type
  itself BEFORE calling print_header().
  This prevents Content-Type from being printed twice.

Usage (from another CGI file):
    # Add cgi-bin folder to path so common.py can be found
    sys.path.insert(0, os.path.dirname(__file__))
    from common import print_header, print_footer

    # Print Content-Type FIRST in your own main
    print("Content-Type: text/html")
    print()

    # Then call print_header - it only prints HTML, not Content-Type
    print_header("Job Search Results")
    # ... your page content here ...
    print_footer()
"""


def print_header(page_title="DrPengsAIIPDemos Job Search"):
    """
    Prints the HTML header for every page.

    Outputs:
      - Opening <html>, <head>, <body> tags
      - Blue title bar with site name (matches professor's demo)
      - Navigation button bar

    NOTE: Content-Type is NOT printed here.
    The calling file must print Content-Type before calling this function.

    Parameters:
        page_title (str) -- the title shown on the browser tab
    """

    # Opening HTML tags - white background like the results page in the demo
    print("<html>")
    print("<head>")
    print("<title>" + page_title + "</title>")
    print("</head>")
    print('<body BGCOLOR="#FFFFFF" LINK="#0088ff" ALINK="#FF0000" VLINK="#CC0000">')

    # Blue title bar - exactly like title.html in the demo
    print('<table width="800" bgcolor="#3366ff">')
    print("<tr>")
    print("    <td>")
    print('        <H1><i><font color="#ffcc00"> DrPengsAIIPDemos.Com </font></i></H1>')
    print("    </td>")
    print("</tr>")
    print("<tr>")
    print("    <td>")
    print('        <font color="#ffffcc">The on-line career and recruitment center')
    print("        dedicated to the high tech industry over the world</font>")
    print("    </td>")
    print("</tr>")
    print("</table>")

    # Navigation button bar - matches the demo buttons exactly
    print('<TABLE CELLSPACING="0" CELLPADDING="3" BORDER="0">')
    print("<tr>")
    print('    <td><a href="/~netid/cgi-bin/home.py">Home</a></td>')
    print('    <td><a href="/~netid/html/job_search.html">Job Search</a></td>')
    print("</tr>")
    print("</TABLE>")
    print("<br>")


def print_footer():
    """
    Prints the HTML footer for every page.

    Outputs:
      - Bottom navigation links (same as demo's print_tailer)
      - Copyright line
      - Closing </body> and </html> tags
    """

    print("<br><br>")
    print("<center>")
    print('<TABLE CELLSPACING="0" CELLPADDING="3" BORDER="0">')
    print("<tr>")
    print('    <td><a href="/~netid/cgi-bin/home.py">Home</a></td>')
    print('    <td><a href="/~netid/html/job_search.html">Job Search</a></td>')
    print("</tr>")
    print("</table>")
    print("<br>")
    print("<i>Copyright &copy; 2026 DrPengsAIIPDemos.com Inc. All rights reserved.</i>")
    print("</center>")
    print("</body>")
    print("</html>")


# -----------------------------------------------
# ONLY runs when you do: python3 common.py
# IGNORED when another file imports this file
# -----------------------------------------------
if __name__ == "__main__":
    print("Content-Type: text/html")
    print()
    print_header("Test Page")
    print("<center><h2>Hello! This is the page content area.</h2></center>")
    print_footer()