#!/usr/bin/perl

#print "Content-Type: text/html\n";
print "Content-Type: text/html\n\n";


#$ENV{'LD_LIBRARY_PATH'} = '/home/oracle/app/oracle/product/11.2.0/dbhome_1/lib';
#$ENV{'ORACLE_HOME'} = '/home/oracle/app/oracle/product/11.2.0/dbhome_1';
#$ENV{'ORACLE_SID'} = 'orclfire';
#$ENV{'LD_LIBRARY_PATH'} = '/opt/oracle/OraHome_1/lib';
#$ENV{'ORACLE_HOME'} = '/opt/oracle/OraHome_1';
#$ENV{'ORACLE_SID'} = 'orcl';

$ENV{'ORACLE_HOME'} = '/usr/lib/oracle/21/client64';
$ENV{'ORACLE_SID'} = 'csdbora';

# Get the current job and member number

$tuple_counts = `/home/qkm28/public_html/cgi-bin/real_time_number`;
#$tuple_counts = `/home/Faculty/peng/public_html/cgi-bin/real_time_number`;

@array = split(" ", $tuple_counts);
$job_number = $array[0];
$member_number = $array[1];
$c_g_number = $array[2];

print <<EOF;

$tuple_counts

<html>
<head>
<title>DrPengsAIIPDemos Job Search</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

</head>
<body BGCOLOR="#00FFFF" LINK="#0088ff" ALINK="#FF0000" VLINK="#CC0000">
<center><h2>DrPengsAIIPDemos Welcomes You! </h2></center>
<center>
<img src="http://newfirebird.cs.txstate.edu/~wp01/img/background.gif" width="550" height="180"  usemap="#map1" border="0"><map name=map1>
<area shape="rect" coords="3,3,215,180" href="http://newfirebird.cs.txstate.edu/~wp01/demo/proc/unix-version/html/job_search.html">
<area shape="rect" coords="310,3, 550,180" href="/~wp01/cgi-bin/employers.pl">
</map>

<br>
<br>
<center>
<i>
Registered Engineers: $member_number<br>
Total jobs: $job_number<br>
Total registered college graduates: $c_g_number<br>
</i>
</center>
<br>

<br>
<b>
DrPengsAIIPDemos.com will assist and challenge you to be where you can be in the 21th centry in the high tech, high competitive, high reward world.
</b>
<br>
<br>
<br>
<table cellspacing="0" cellpadding="3" border="0">
<tr>
	<td> <a href="/~wp01/cgi-bin/home.pl"> Home </a>
	<td> <a href="http://newfirebird.cs.txstate.edu/~wp01/demo/proc/unix-version/html/job_search.html">Job Search </a>
        <td> <a href="http://newfirebird.cs.txstate.edu/~wp01/demo/proc/unix-version/html/employer_login.html">Employers </a>
        <td> <a href="http://newfirebird.cs.txstate.edu/~wp01/demo/proc/unix-version/html/member_login.html">Members </a>
</tr>



</table>
</center>


<br>
	<i>Copyright \@2023 DrPengsAIIPDemos.com Inc. All rights reserved.
	</i>
</body>
</html>
EOF
