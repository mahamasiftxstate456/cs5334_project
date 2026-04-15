#!/usr/local/bin/perl
#
# Created:  01/23/2001
# Modified: 03/30/2003
#           02/11/2012

#$ENV{'LD_LIBRARY_PATH'} = '/opt/oracle/OraHome_1/lib';
#$ENV{'ORACLE_HOME'} = '/opt/oracle/OraHome_1';
#$ENV{'ORACLE_SID'} = 'orcl';

$ENV{'LD_LIBRARY_PATH'} = '/home/oracle/app/oracle/product/11.2.0/dbhome_1/lib';
$ENV{'ORACLE_HOME'} = '/home/oracle/app/oracle/product/11.2.0/dbhome_1';
$ENV{'ORACLE_SID'} = 'orclfire';

$debug=0;

%row_color = ();
$row_color{"#ffffcc"} = "#ccffff";
$row_color{"#ccffff"} = "#ffffcc";

sub log{
	local($file)="./fff.log";
	if($debug){
		open(FILE, ">$file");
		print FILE $_;
		print FILE "\n";
		close(FILE);
	}
}

sub get_parameters{
	local( *contents ) = @_;
	if( $ENV{'REQUEST_METHOD'} eq 'GET' && "$ENV{'QUERY_STRING'}" ne ''){
		$buffer = "$ENV{QUERY_STRING}";
#		print $buffer;
	}
	elsif( $ENV{'REQUEST_METHOD'} eq 'POST' ){
		read( STDIN, $buffer, "$ENV{'CONTENT_LENGTH'}");
#		print "post; $buffer';
	}

	foreach $pair(split("&", "$buffer")){
		# Get name , value pair strings
		($name, $value) = split(/=/,$pair);
		#Translage "+" to white space
		$value =~ tr/+/ /;
		#Decipher ASCII hexadecimal escape characters
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		#Add the pair to parameter list
		$contents{$name} = $value;
		#print "name=$name, value=$value, $contents{$name}=$value\n";
	}
}


sub print_header{
	print "<html>\n";
	print "<head> <title>Job Search Results</title> </head>\n";
	print "<body bgcolor=\"#FFFFFF\">\n";
}

sub print_tailer{

print <<EOF;
<center>
<table cellspacing="0" cellpadding="3" border="0">
<tr>
	<td> <a href="/~wp01/cgi-bin/home.pl">Home </a>
	<td> <a href="/~wp01/demo/proc/unix-version/html/job_search.html">Job Search </a>
	<td> <a href="/~wp01/demo/proc/unix-version/html/employer_login.html"> Employers </a>
	<td> <a href="/~wp01/demo/proc/unix-version/html/member_login.html">Members </a>

</tr>
</table>
</center>

EOF

print "</body>\n";
print "</html>\n";
print "\n";
}


return 1;
