#!/usr/bin/perl
# This program take the input from user on the job search page and
# get the matched job from the database before display them back
# onto the screen
#
# Created: 10/12/2000
# Modifed: 01/30/2001
#          02/19/2003
#          03/26/2003
#          10/16/2003
#          02/21/2005
#          04/06/2006
#
#          03/29/2008
#          02/23/2012
#          03/14/2016
#          03/10/2023


require "./common.cgi";

sub query_job{
	local( $i,$j,$string );
	local($s1, @s2);
	local($ltype, $lvalue);
	$string="job_type=$contents{job_type}&";
    	$string= $string."job_title=$contents{job_title}&";
	$string =$string."specialization=$contents{specialty}&"; 
	$string = $string."company_name=$contents{company_name}&"; 
	$ltype = $contents{location_type};
	$lvalue = $contents{$ltype};
	$string = $string."$ltype=$lvalue&";

	$requested_page_number = $contents{requested_page_number};

	if( $contents{salary} eq "Any" ){
		$s1 = "Any";
	}
	else{
		@s2 = split(/-/, $contents{salary});
		$s1 = $s2[0]."0000";
	}
	$string = $string."min_salary=$s1"; 

	$comfile = "/home/qkm28/public_html/cgi-bin/ematch_job \"$string\" 1";

	print "command: $comfile\n";
# #
# Execute the job search executable
	#if ( !$requested_page_number )
	#{
	$proc_returns = `$comfile`;

	#}
        @array_proc_returns = split (' ', $proc_returns, 2);

        $total_matched_rows = $array_proc_returns[0];

	$page_size = 16;

	$actual_page = $total_matched_rows / $page_size;
	$total_page  = int $total_matched_rows / $page_size;

	if( $total_page < $actual_page ){
		$total_page ++; 
	}

	if ($requested_page_number == "")
	{
		$current_page_number = 1;
	} elsif ($requested_page_number > $total_page )
	{
		$current_page_number = $total_page;
	}
	else
	{
		$current_page_number = $requested_page_number;
	}

	#@tr_results_array = split ("<tr ", $array_proc_returns[1]);
	@tr_results_array = split ("LINE ", $array_proc_returns[1]);

	$start_entry = $page_size * ($current_page_number - 1)+1;

	
	$temp_rows = "";
	#$temp_rows = "" . " <tr><td>" . "requested_page_number=".$requested_page_number."; page_size=" . $page_size ."; currnt_page_number=". $current_page_number."; start_entry=". $start_entry . "</td></tr>\n";
	for ($i=$start_entry; (($i-$start_entry < $page_size) || (($start_entry == 0)&&($i-$start_entry <= $page_size))) && $i <= $total_matched_rows; $i++)
	{
		if ( $tr_results_array [$i] )
		{
			$temp_rows .= "<tr name=\"matched_job_num\" bgcolor=\"#FFFFCC\"> <td>". $i. "</td>";
			#$temp_rows .= "<tr > <td>". $i. "</td>";
			#$tr_results_array[$i] =~ tr/LINE / /;
			$temp_rows .= $tr_results_array [$i];
			#$temp_rows .= "<tr name=\"added\" ". $tr_results_array [$i];
		}
		#$temp_rows .= "<tr><td>i=$i,start_entry=$start_entry,$current_page_number,$requested_page_number</td></tr>\n";
	}
	return "$temp_rows";
	return "$array_proc_returns[1]";
}


sub print_job{
	local($flag) = 0;
	local(@array);
	local($dir) = `pwd`;
	local($color) = "#ffffcc";

#	print table head
	print "<center>\n";
	print "<table >\n";
	print "<th>Job Number\n";
	print "<th>Rating\n";
	print "<th>Job Title\n";
	print "<th>Special field\n";
	print "<th>Location\n";
	print "<th>Company\n";
	print "<th>Salary Range\n";
	#print "temp_results_a[0]=$temp_results_a[0]";
	#print "temp_results_a[1]=$temp_results_a[1]";
	#print "temp_results_a[2]=$temp_results_a[2]";
	#print "$proc_returns";
	print "$query_job_returns";

	print "</table>\n";
	print "</center>\n";
}

$ENV{'ORACLE_HOME'} = '/usr/lib/oracle/21/client64';
$ENV{'ORACLE_SID'} = 'csdbora';

#&print_header;

&get_parameters( *contents );

$query_job_returns = &query_job;

print "Content-Type: text/html\n\n";


&print_header;

print "<center><h2>Job search results</h2> (Total $total_matched_rows matches)</center>\n";

&print_job($query_job_returns);
$filename =~ tr/ /+/;

#print "(Page $current_page_number of $total_page in file $filename)<br>";
print "(Page $current_page_number of $total_page)<br>";


# print the pre/next page href

if ( $current_page_number < $total_page ){
	$next_page = $current_page_number + 1;
	print "<a href='/~wp01/cgi-bin/jobsearch.pl?$ENV{QUERY_STRING}&requested_page_number=$next_page'>Next Page > </a>";
} else
{
	print "Next Page >";
}

print "<br>";

if ( $current_page_number > 1 ){
	$prepage = $current_page_number -1;
	print "<a href='http://newfirebird.cs.txstate.edu/~wp01/cgi-bin/jobsearch.pl?$ENV{QUERY_STRING}&requested_page_number=$prepage'>Previous Page < </a>";
} else
{
	print "Previous Page >";
}

print "<br>";

if ($total_page > 1)
{
	print "Goto page: ";
	for ($i=0; $i < $total_page; $i++)
	{
		$page_number = $i+1;
		if ($page_number == $current_page_number) 
		{
		   print "$page_number ";
		}
		else
		{
		   print "<a href='/~wp01/cgi-bin/jobsearch.pl?$ENV{QUERY_STRING}&requested_page_number=$page_number'>$page_number</a>";
		}
		print " ";
	}
}

&print_tailer;


