

/*  Created:   01/20/2002
 *  Modified:  03/24/2003
 *             04/01/2003
 *             02/21/2005
 *             04/06/2006
 *             03/31/2010
 *             02/14/2012
 */

#include "ematch_class.h"
#include "ematch_const_struct.h"
#include <algorithm>

ematch_class::ematch_class()
{
	pair_number = 0;
	location_search_type = 0;

	total_selected_rows = 0;
	total_matched_rows = 0;

	salary_required = 1;
	degree_required = 0;
	year_of_exp_required = 0;
	do_not_set_search_by_c_r_s_or_city = 0; // for member search

	asked_max_salary = 0;
}


ematch_class::ematch_class(int e_or_i)
{
	// cout << "Initialize ematch_class with e_or_i = " << e_or_i << endl;

	ematch_or_insert = e_or_i;
	pair_number = 0;
	location_search_type = 0;

	total_selected_rows = 0;
	total_matched_rows = 0;

	salary_required = 0;
	degree_required = 0;
	year_of_exp_required = 0;
	do_not_set_search_by_c_r_s_or_city = 0; // for member search

	if (e_or_i == EMATCH_) {
		asked_max_salary = 0;
	}
}

//
//
void ematch_class::set_initial_environ(int table_indx,
			int search_typ,
			int country_cod)
{
	int i;

	//cout << "Initialize first enviroment of ematch_class with "<< table_indx
	//			<< " and country_code = " << country_cod << endl;

	search_type = search_typ;
	country_code = country_cod;

	if ((search_type == JOB_SEARCH_1) || (search_type == JOB_SEARCH_2)) {
		my_search_type = JOB_SEARCH;
	} else if
		((search_type == MEMBER_SEARCH_1)||(search_type == MEMBER_SEARCH_2)) {
		my_search_type = MEMBER_SEARCH;
	}

	column_number = column_number_for_tables[table_indx-1];
	
	table_index = table_indx;


	max_matching_number = MAX_MATCH_NUMBER;


	column_listed = new int [column_number];

	name_index = new int [column_number];
	name_to_column_index = new int [column_number];

	for (i = 0; i < column_number; i++)
		column_listed[i] = 0;

}

//
////
void ematch_class::set_initial_insert_environ(int table_indx)
{
	int i;

	//cout << "Initialize first enviroment of ematch_class with "<< table_indx
	//			<< " and country_code = " << country_cod << endl;

	column_number = column_number_for_tables[table_indx-1];
	
	table_index = table_indx;

	column_listed = new int [column_number];

	name_index = new int [column_number];
	name_to_column_index = new int [column_number];

	for (i = 0; i < column_number; i++)
		column_listed[i] = 0;

}

/*
 *  It will extract each substring of the form 'a=b' in a CGI parameter
 *  to the public variable cgi_string_pairs (char array) in class ematch_class
 *
 *  Before calling the function, the function  find_pair_number() must
 *  be called first. That function will find the number of pairs and
 *  will also allocate space to the variable cgi_string_pairs
 *
 *  When s_type == -1, this function is called not for ematch search.
 *  Instead, it is  called for cases such as insert_table()
 */
void ematch_class::extract_cgi_pairs (ostream &out, mystring whole_cgi_string)
{

	char *temp_str, *string_left;

	int p_len = 0, exit_flag = 0;
	
	int i = 0, str_len;
	my_string_class my_string_instance;


	if (my_string_instance.is_a_blank_string (whole_cgi_string))
			   // Empty string. Do nothing
		 return;

	find_pair_number(out, whole_cgi_string);  // find number of name=value pairs

	str_len = strlen(whole_cgi_string) + 1;

	if (str_len > MAX_STRING_LENGTH) {

		out << "Error: string length exceeds maximum allowed " << MAX_STRING_LENGTH << endl;
		exit(1);

	}
	out << "In eeeextract_cgi_pairs\n";
	out << "str_len is " << str_len << endl;

	string_left = new char[str_len];
	temp_str = new char [str_len];
	cgi_string = new char [str_len];

	strcpy(cgi_string, whole_cgi_string);
	strcpy(temp_str, whole_cgi_string);

	out << "cgi_string=" << cgi_string << ", pair_number = " << pair_number <<  endl;


	while (1) {

		out << " i = " << i << " temp_str=" << temp_str << "@@" <<  endl;
		string_left = strchr(temp_str, '&');


		if (!string_left) {       // last argument
			out << "Last argument" << endl;
			exit_flag = 1;      
			p_len = strlen(temp_str);

		} else {
			p_len = strlen(temp_str) - strlen(string_left);
			out << "string_left ^^"<< string_left << "^^" << endl;
		}
		//out << "calling remove_trailing_space_chars" << endl;
		//my_string_instance.remove_trailing_space_chars (temp_str);

		cgi_string_pairs[i] = new char[p_len+1];

		strncpy(cgi_string_pairs[i], temp_str, p_len);

		(cgi_string_pairs[i])[p_len] = '\0';


		i++;
		// out << "exit_flag=" << exit_flag<< endl;
		out << "string " << i << " has " << p_len << " char, and is:" 
					<< cgi_string_pairs[i-1] << "--";
		out << "  and its length is:" << strlen(cgi_string_pairs[i-1]) << endl;
		if (exit_flag == 1) {

			out << "exit_flag == 1 -- reached end of list " << endl;
			out << "exit from extract_cgi_pairs" << endl;
	    		break;
		}
		else {
			out << "string_left=" << string_left << "---" << endl;
			out << "temp_str=" << temp_str << "===" << endl;
			temp_str = string_left + 1;
			out << "adjusted temp_str=" << temp_str << endl;
		}

	} 

	//out << "BEFORE Calling separate_each_pair \n";

	//separate_each_pair(out);

	 out << " Returning from extract_cgi_pairs" << endl;
} // end of ematch_class::extract_cgi_pairs


// Find the number of charater '&' separated strings (parameters) in a given
// CGI string 
// Note: This function is used so that the function extract_cgi_strings
//       can handle any number of strings in a given CGI string.
//       It is merely for flexility and robustness
// Created: 02/11/2000
//
void ematch_class::find_pair_number (ostream &out, mystring whole_cgi_string)

{

	mystring temp_str, string_left;

	int p_len = 0, exit_flag = 0;

	int k = 0;   // number of parameters found


 
	string_left = new char[MAX_STRING_LENGTH];

	temp_str = new char [MAX_STRING_LENGTH];


	strcpy(temp_str, whole_cgi_string);

	 while (1) {

		out << "temp_str=" << temp_str << endl;
		while (temp_str[0] == ' ')  // get rid of extra spaces
			temp_str++;

		string_left = strchr(temp_str, '&');


		if (!string_left) {       // last argument
			exit_flag = 1;      
			p_len = strlen(temp_str);

		} else
			p_len = strlen(temp_str) - strlen(string_left);

		k++;

		if (exit_flag == 1) {
			   out << "Reached end of list, exit ...\n";
	    	   break;
		}
		else {
			temp_str = string_left + 1;
		}

		// k++;
	} 
	cgi_string_pairs = new mystring[k];  // allocate memory for addresses of all pairs
	name = new mystring[k];              // allocate memory for addresses of all names
	value = new mystring[k];             // allocate memory for addresses of all values
	value_type = new mystring[k];

	unchanged_value = new mystring[k];

	pair_number = k;
	keyword_number = k;

	 out << " Returning from find_pair_number. Set pair_number to " << pair_number << endl;

}  // end of ematch_class::find_pair_number


/*
 * This private member  separates each pair of the form
 * 'name=value' in an array to two array, an name array
 * and a value array, both defined in a ematch_class  
 * instance.
 *
 * It is assumed there are no space characters around
 * 'name' or 'value'
 *
 */
void ematch_class::separate_each_pair (ostream &out)

{
	int i, j, m, old_j;
	int k, str_len, pair_len;

	mystring n, v;
	int actual_pair_number = 0;
	my_string_class my_string_instance;

	out << "BBEGINNING of separate_each_pair in ematch_class\n";

	str_len = strlen(cgi_string);


	asked_min_salary = asked_max_salary = 0;

	n = new char[str_len];
	v = new char[str_len];

	old_j = -1;
	j = 0;

	for (i=0; i < pair_number; i++) {


		pair_len = strlen(cgi_string_pairs[i]);

		v = strchr(cgi_string_pairs[i], '=');


		k = strlen(v);


		if (j > old_j) {
			name[j]  = new char[pair_len - k + 1];
			value[j] = new char[2*k];
			unchanged_value[j] = new char[2*k];
			value_type[j] = new char[2];
		}

		old_j = j;

		strncpy(name[j],  cgi_string_pairs[i], pair_len-k);
		strncpy(value[j], v+1, k-1);
		strncpy(unchanged_value[j], v+1, k-1);

		(name[j])[pair_len-k] = '\0';
		(value[j])[k-1] = '\0';
		(unchanged_value[j])[k-1] = '\0';

		convert_a_single_quote_and_percent_sign(value[j]);

		my_string_instance.to_lower(name[j]);  // Convert every char to lower case

		if (ematch_or_insert == EMATCH_)					// Ematch call
			my_string_instance.to_lower(value[j]);  // Convert to lower case

		out << "name=" << name[j] << " and value = " << value[j] << endl;

		convert_a_job_table_column_name(name[j]);

		m = find_column_index(name[j]);
		if (m < 0) {
			if ((ematch_or_insert == EMATCH_) &&
				(my_search_type == MEMBER_SEARCH)) {

				if (strcmp(name[j],"min_salary") == 0) {
					if (strcmp(unchanged_value[j], "Any") == 0)
						salary_required = 0;
					else 
						asked_min_salary = atoi(value[j]);
					continue;
				}
				else if (strcmp(name[j],"max_salary") == 0) { 
					if (strcmp(unchanged_value[j], "Any") == 0)
						salary_required = 0;
					else 
						asked_max_salary = atoi(value[j]);
					continue;
				}
			}
			out << "Invalid column name: " << name[j] << endl;
			exit (-1);
		} else
			out << "Column name: " << name[j] << ", index m = " << m << endl;

		column_listed[m] = 1;
		name_index[m] = j;

		if (table_index == JOB_TABLE_INDEX) {
			strcpy(value_type[j], job_table_column_quotes[m]);
		}

		if ((ematch_or_insert == EMATCH_) &&
			(my_search_type == JOB_SEARCH) && (m == JOB_TABLE_MIN_SALARY)) {
			if (strcmp(unchanged_value[j], "Any") == 0) {
				salary_required = 0;

			} 
		} else if ((ematch_or_insert == EMATCH_) &&(my_search_type == MEMBER_SEARCH)) {
			if (strcmp(name[j],"min_salary") == 0)
				if (strcmp(unchanged_value[j], "Any") == 0) {
					salary_required = 0;

				} else 
					asked_min_salary = atoi(value[j]);
			else if (strcmp(name[j],"max_salary") == 0) 
					asked_max_salary = atoi(value[j]);
		}

		if ((ematch_or_insert == EMATCH_) &&
					(my_search_type == MEMBER_SEARCH)
						&& (m == MEMBER_TABLE_YEAR_OF_EXP)) {
			if (strcmp(unchanged_value[j], "Any") == 0)
				year_of_exp_required = 0;
		}

		if ((ematch_or_insert == EMATCH_) &&
					(my_search_type == MEMBER_SEARCH)
						&& (m == MEMBER_TABLE_DEGREE)) {
			if (strcmp(unchanged_value[j], "Any") == 0)
				degree_required = 0;
		}

		out << "COLUMN " << m << " with name " << name[j] << " at position "
					<< j << " listed" << endl;

		// By pass name=All pair
		if ((my_search_type == MEMBER_SEARCH) && 
					(m == MEMBER_TABLE_CURRENT_JOB_LOCATION_CODE) &&
					(do_not_set_search_by_c_r_s_or_city))
				;
		else if ((strcmp(value[j], "All") != 0) && (strcmp(value[j], "all") != 0))
			j++;
		else if ((my_search_type == MEMBER_SEARCH) && 
					(m == MEMBER_TABLE_CURRENT_JOB_LOCATION)) {
			out << "current_job_location=" <<
					value[j] << "+" << endl;

				location_search_type = 0;
				// So that the desired_job_location_code value will be
				//    ignored.
				do_not_set_search_by_c_r_s_or_city = 1;
		}

	}

	out << "salary_required = " << salary_required << endl;
	out << " Returning from separate_each_pair in ematch_class \n";

	pair_number = j;

} // ematch_class::ematch_class::separate_each_pair ()

//
// Return the table name, determined by the value of the variable 'table_index', which
//   gets its value from constructor
//
void ematch_class::get_table_name (mystring table_name)
{
	strcpy (table_name, table_names[table_index-1]);
	return;
}

/*
 *  Convert a single quote char to two single quote chars and a percent
 *		sign char to \%
 *  These are needed so that the data can be inserted into ORACLE 
 */
void ematch_class::convert_a_single_quote_and_percent_sign(mystring s)
{
	int i,j, k;
	mystring temp_s;

	k = strlen(s);

	temp_s = new char [2*k];
	strcpy (temp_s, "");

	for (i=0, j=0; i < k; i++, j++) {
		temp_s[j] = s[i];
		if (s[i] == '\'')
			temp_s[++j] = '\'';
		else if (s[i] == '%') {
			temp_s[j] = '\\';
			temp_s[++j]  = s[i];
		}
	}
	temp_s[j] = '\0';

	strcpy (s, temp_s);

}

void ematch_class::convert_a_job_table_column_name(mystring a_column_name)
{
	if (table_index == JOB_TABLE_INDEX) {
		if ( !strcmp(a_column_name, "title"))
			strcpy(a_column_name, "job_title");
		else if ( !strcmp(a_column_name, "specialty"))
			strcpy(a_column_name, "specialization");
		else if ( !strcmp(a_column_name, "specialized_field"))
			strcpy(a_column_name, "specialization");
		else if ( !strcmp(a_column_name, "low_salary"))
			strcpy(a_column_name, "min_salary");
		else if ( !strcmp(a_column_name, "high_salary"))
			strcpy(a_column_name, "max_salary");
		else if ( !strcmp(a_column_name, "country"))
			strcpy(a_column_name, "country_code");
		else if ( !strcmp(a_column_name, "country"))
			strcpy(a_column_name, "country_code");
		else if ( !strcmp(a_column_name, "region"))
			strcpy(a_column_name, "region_name");
		else if ( !strcmp(a_column_name, "state"))
			strcpy(a_column_name, "state_name");
		else if ( !strcmp(a_column_name, "city"))
			strcpy(a_column_name, "location");
		else if ( !strcmp(a_column_name, "company"))
			strcpy(a_column_name, "company_name");
		else if ( !strcmp(a_column_name, "reference"))
			strcpy(a_column_name, "reference_num");
		else if ( !strcmp(a_column_name, "contact"))
			strcpy(a_column_name, "contact_person");
	} else if (table_index == MEMBER_TABLE_INDEX) {
		if ( !strcmp(a_column_name, "login_name"))
			strcpy(a_column_name, "login_id");
		else if ( !strcmp(a_column_name, "specialty"))
			strcpy(a_column_name, "specialization");
		else if ( !strcmp(a_column_name, "specialized_field"))
			strcpy(a_column_name, "specialization");
		else if ( !strcmp(a_column_name, "current_location"))
			strcpy(a_column_name, "current_job_location");
		else if ( !strcmp(a_column_name, "current_location_code"))
			strcpy(a_column_name, "current_job_location_code");
		else if ( !strcmp(a_column_name, "salary"))
			strcpy(a_column_name, "desired_salary");
		else if ( !strcmp(a_column_name, "location"))
			strcpy(a_column_name, "desired_job_location");
		else if ( !strcmp(a_column_name, "location_code"))
			strcpy(a_column_name, "desired_job_location_code");
		else if ( !strcmp(a_column_name, "job_title"))
			strcpy(a_column_name, "current_job");
	}
}

int ematch_class::validate_table_column_names(void)
{
	int i, j, k;
	int flag;
	int total_invalid=0;
		

	for (i=0; i < pair_number; i++) {
		flag = 1;
		if (table_index == JOB_TABLE_INDEX) // For job search, do not call the
				//  function find_column_index() for efficiency
			for (j = 0; j < COLUMN_NUMBER_IN_JOB_TABLE; j++) {

				if ( !strcmp(name[i], job_table_column_names[j])) {
					flag = 0;
					break;
				}
				else {

					k = find_column_index(name[i]);
					if (k >= 0 ) flag = 0;
			
				}
			}
		else if (table_index == MEMBER_TABLE_INDEX) 
					//  function find_column_index() for efficiency
			for (j = 0; j < COLUMN_NUMBER_IN_MEMBER_TABLE; j++) {

				if ( !strcmp(name[i], member_table_column_names[j])) {
					flag = 0;
					break;
				}
				else {
					k = find_column_index(name[i]);
					if (k >= 0 ) flag = 0;
				}
			}
		if (flag) {
			cout << "Invalid column name: " << name[i] << endl;
			total_invalid++;
		}
	}
	if (total_invalid > 0) {
		cout << "Total " << total_invalid << " column names!\n";
		return(-total_invalid);
	}
	return(0);
}

int ematch_class::find_column_index(mystring a_name)
{
	int i = 0;


	if (table_index == JOB_TABLE_INDEX) 
		for (i = 0; i < column_number; i++) {

			if (strcmp (a_name, job_table_column_names[i]) == 0)
				return i;
		}
	else if (table_index == MEMBER_TABLE_INDEX) 
		for (i = 0; i < column_number; i++) {

			if (strcmp (a_name, member_table_column_names[i]) == 0)
				return i;
		}
	else if (table_index == EMPLOYER_TABLE_INDEX)
		for (i = 0; i < column_number; i++) {

			if (strcmp (a_name, employer_table_column_names[i]) == 0)
				return i;
		}

	return -1;

}

/*
 * Used by member search
 */
int ematch_class::find_degree_index(mystring degree_name)
{
	int i = 0, j;
	my_string_class my_string_instance;

	mystring s1;

	j = strlen(degree_name);

	s1 = new char[j+1];

	strcpy (s1, degree_name);
	my_string_instance.to_lower(s1);

	for (i = 0; i < NUMBER_OF_DEGREE_TYPE; i++) {
		if (strcmp(s1, degree_names_in_lower_case[i]) == 0) {
			delete s1;
			return i;
		}

	}
	delete s1;
	return -1;
};


/*
 *
 */

void ematch_class::set_num_of_rows(int i)
{
	total_matched_rows = i;
}

void ematch_class::set_more_ematch_environ(ostream &out, 
							int search_method)
{
	int i;

	my_string_class string_instance;


	location_search_type = search_method;


	if (country_code == USA) {
		neighbor_city_beginning_index[0] = 0;
		neighbor_state_beginning_index[0] = 0;
		us_city_in_state_beginning_index[0] = 0;
		us_state_in_region_beginning_index[0] = 0;

		for (i = 1; i< NUMBER_OF_US_CITIES; i++) {
			neighbor_city_beginning_index[i] =
					neighbor_city_beginning_index[i-1] +
							2*us_neighbor_city_number[i-1];
		}

		for (i = 1; i< NUMBER_OF_US_STATES; i++) {
			us_city_in_state_beginning_index[i] =
					us_city_in_state_beginning_index[i-1] + 
						us_cities_in_states_number[i-1];
		}

		for (i = 1; i< NUMBER_OF_US_STATES; i++) {

			neighbor_state_beginning_index[i] =
					neighbor_state_beginning_index[i-1] +
						2*us_neighbor_state_number[i-1];
		}

		for (i = 1; i< NUMBER_OF_US_REGIONS; i++) {
			us_state_in_region_beginning_index[i] =
					us_state_in_region_beginning_index[i-1] + 
					us_states_in_regions_number[i-1] + 1;
		}
	}

	asked_city_index = -1;
	asked_state_index = -1;
	asked_region_index = -1;

	if ((search_type == JOB_SEARCH_1) || 
			(search_type == JOB_SEARCH_2)) {

		out << "column_listed[JOB_TABLE_CITY]=" << column_listed[JOB_TABLE_CITY] << endl;
		out << "column_listed[JOB_TABLE_STATE_NAME]=" << column_listed[JOB_TABLE_STATE_NAME] << endl;
		out << "column_listed[JOB_TABLE_REGION_NAME]=" 
				<< column_listed[JOB_TABLE_REGION_NAME] << endl;

		asked_location_name = new char [JOB_TABLE_LOCATION_LENGTH];

		if (column_listed[JOB_TABLE_LOCATION]) {

			asked_city = new char [JOB_TABLE_LOCATION_LENGTH];
			strcpy (asked_city, value[name_index[JOB_TABLE_CITY]]);
			string_instance.to_lower(asked_city);
			asked_city_index = find_city_index(asked_city);
			strcpy (asked_location_name, asked_city);
			asked_location_index = asked_city_index;
		}
		if (column_listed[JOB_TABLE_STATE_NAME]) {

			asked_state = new char [JOB_TABLE_STATE_NAME_LENGTH];
			strcpy (asked_state, value[name_index[JOB_TABLE_STATE_NAME]]);
			string_instance.to_lower(asked_state);
			asked_state_index = find_state_index(asked_state);
			strcpy (asked_location_name, asked_state);
			asked_location_index = asked_state_index;
		}

		if (column_listed[JOB_TABLE_REGION_NAME]) {

			asked_region = new char [JOB_TABLE_REGION_NAME_LENGTH];
			strcpy(asked_region, value[name_index[JOB_TABLE_REGION_NAME]]);
			string_instance.to_lower(asked_region);
			asked_region_index = find_region_index(asked_region);
			strcpy (asked_location_name, asked_region);
			asked_location_index = asked_region_index;
		}

		/*if (salary_required) {
			
			out << "set asked_min_salary=";
			asked_min_salary = atoi(value[name_index[JOB_TABLE_MIN_SALARY]]);
			out << asked_degree << endl;

		}*/
	}
	else if ((search_type == MEMBER_SEARCH_1)
			|| (search_type == MEMBER_SEARCH_2)) {

		if (search_method == 2) {
			asked_region = new char [MEMBER_TABLE_CURRENT_JOB_LOCATION_LENGTH];
			strcpy(asked_region, value[name_index[MEMBER_TABLE_CURRENT_JOB_LOCATION]]);
			asked_region_index = find_region_index(asked_region);
		} else 	if (search_method == 3) {
			asked_state = new char [MEMBER_TABLE_CURRENT_JOB_LOCATION_LENGTH];
			strcpy(asked_state, value[name_index[MEMBER_TABLE_CURRENT_JOB_LOCATION]]);
			asked_state_index = find_state_index(asked_state);
		} else 	if (search_method == 4) {
			asked_city = new char [MEMBER_TABLE_CURRENT_JOB_LOCATION_LENGTH];
			strcpy(asked_city, value[name_index[MEMBER_TABLE_CURRENT_JOB_LOCATION]]);
			asked_city_index = find_city_index(asked_city);
		}

		if (year_of_exp_required)
			asked_year_of_exp = atoi(value[name_index[MEMBER_TABLE_YEAR_OF_EXP]]);
		if (salary_required) {
			/* min or max salary is not part of the member table.
			 * Have to make column_listed[MEMBER_TABLE_DESIRED_SALARY] = 1 so
			 * that the MEMBER_TABLE_DESIRED_SALARY column in each candidate
			 * tuple will be checked when being rated.
			 */
			column_listed[MEMBER_TABLE_DESIRED_SALARY] = 1; 
			if (asked_max_salary == 0)
				asked_max_salary = asked_min_salary;
		}
		if (degree_required) {
			asked_degree = find_degree_index(value[name_index[MEMBER_TABLE_DEGREE]]);
			if (asked_degree < 0)
				out << "Error: Invalid degree --" <<value[name_index[MEMBER_TABLE_DEGREE]]
					<< "--" << endl;
			out << "ASKED DEGREE=" << asked_degree << endl;
		}
	}
}

void ematch_class::insert_a_column_to_result_array(mystring a_col,
									int column_pos, int row_index,
									int ind)
{

	int str_len;

	str_len = strlen(a_col);

	result_array[row_index-1][column_pos] = new char [str_len+1];
	strcpy (result_array[row_index-1][column_pos], a_col);

	result_array_ind[row_index-1][column_pos] = (int) ind;

	if (output_width[column_pos] < str_len)
		output_width[column_pos] = str_len;

}

void ematch_class::initialize_result_array(void)
{
	int i, j;

	result_array = new mystringstring [max_matching_number];
	for (i = 0; i < max_matching_number; i++)
		result_array[i] = new mystring [column_number];

	result_array_ind = new int * [max_matching_number];

	original_index = new int [max_matching_number];

	for (i = 0; i < max_matching_number; i++) {
		result_array_ind[i] = new int [column_number];

		original_index[i] = i;

		for (j = 0; j < column_number; j++)
			result_array_ind[i][j] = -1;  // default to NULL for each ind var
	}

	output_width = new int[column_number];

	for (i = 0; i < column_number; i++)
		output_width[i] = 0;
	
	ratings = new int [max_matching_number];
	for (i = 0; i < max_matching_number; i++)
		ratings[i] = 100;

}

void ematch_class::set_output_width(int column_pos, int current_width)
{
	if (output_width[column_pos] < current_width)
		output_width[column_pos] = current_width;
}

void ematch_class::print_result_rows(ostream &out)
{
	int i, j, k, l;
	my_string_class my_string_instance;

	cout << total_matched_rows << " \n";

	for (i=0; i < total_matched_rows; i++) {

		k = original_index[i];

		if (ratings[i] > 0) {
			out << "Row " << i+1 << endl;
			out << "Rating = " << ratings[i] << endl;

			for (j=0; j < column_number; j++) {
				if ((my_search_type == MEMBER_SEARCH) &&
								(j == MEMBER_TABLE_DEGREE) &&
								(my_string_instance.is_digit(result_array[k][j])) &&
								(!my_string_instance.is_a_blank_string(result_array[k][j]))) {
					l = atoi(result_array[k][j]);	
					out << setw (output_width[j]) << degree_names[l]  << "&";
				}
				else
					out << setw (output_width[j]) << result_array[k][j]  << "&";

				// out << setw (output_width[j]) << result_array[i][j]  << " ind="
				//					<< result_array_ind[i][j] << ", ";
			}
			out << endl;
                        ///cout << "\n";
                        //cout.put('<');
                        //cout << "tr > <td>";
                        //cout << "<tr> <td>";
                        cout << "LINE ";
                        cout << "<td>" << ratings[i] << "</td>\n";
                        //cout << ratings[i] << "</td>\n";
                        cout << "<td><a href='/~wp01/cgi-bin/getjob.pl?id="<<result_array[k][0]<<
				"&job_title=" << result_array[k][2] <<
				"&specialty=" << result_array[k][3] <<
				"&location=" << result_array[k][7] <<
				"&company=" << result_array[k][10] <<
				"&salary=" << result_array[k][8] << "-" << result_array[k][9] <<
				"' target=display>" << result_array[k][2] << "</a></td>\n";
                        cout << "<td>" << result_array[k][3] << "</td>\n";
                        cout << "<td>" << result_array[k][7] << "</td>\n";
                        cout << "<td>" << result_array[k][10] << "</td>\n";
                        cout << "<td>" << result_array[k][8] << "-" << result_array[k][9] << "</td>\n";
                        cout << "</tr>\n";

		}
	}

}

/* Sort the list of output tuples in ascending order of their ratings.
 * For efficiency consideration, sorting is done in place -- only the
 * ratings array is rearranged and the order of elements of result_array
 * is unchanged. The array original_index keeps the index of the final
 * sorted order. That is, if original_index[i] == k, then the ith
 * output tuple is in the kth position of result_array.
 */
void ematch_class::sort_result_rows(ostream &out)
{
	int i, j, k;
	int max_index;


	out << "In sort_result_rows, total_matched_rows=" << total_matched_rows << endl;
	for (i=0; i < total_matched_rows; i++)
		out << i << ":" << ratings[i] <<", ";
	out << endl;

	for (i=0; i < total_matched_rows; i++) {

			out << "Row " << i << endl;
			out << "Rating = " << ratings[i] << endl;;

			max_index = i; 
			
			for (j=i+1; j < total_matched_rows; j++) {
				out << "Compare with row " << j << " with rating = " << ratings[j] << endl;
			
				if (ratings[j] > ratings[max_index]) {
					
					out << "j=" << j << ",max_index=" << max_index <<
						",ratings[j]=" << ratings[j] << 
						"> ratings[max_index]=" << ratings[max_index] << endl;
					max_index = j;
				}
			}
			
			// out << "SWAP " << i << " and " << max_index << endl;


			out << max_index << " <==> " << i << " with " <<
				ratings[max_index] << " <==> " << ratings[i] << endl;

			k = original_index[max_index];
			original_index[max_index] = original_index[i];
			original_index[i] = k;

			k = ratings[max_index];
			ratings[max_index] = ratings[i];
			ratings[i] = k;

			// out << endl;

	}

}



int ematch_class::the_state_is_in_the_region(int state_indx, int region_indx, ostream &out)
{
	int i, k;
	int in_it = 0;

	k = us_state_in_region_beginning_index[region_indx];
	//limit = us_states_in_regions_number[region_indx];

	out << "Beginning index for region " << us_regions[region_indx] << " is "
			<< k << endl;

	for (i = 0; us_states_in_regions[k+i] >= 0; i++) {

		out << "Check state with index " << us_states_in_regions[k+i] <<
			" and it should be state " << us_states[us_states_in_regions[k+i]] << endl; 
		if (state_indx == us_states_in_regions[k+i]) {
			in_it = 1;
			break;
		}

	}

	out << "Number of states is " << i  << endl;
	return in_it;
}


int ematch_class::the_city_is_in_the_state(int city_indx, int state_indx, ostream &out)
{
	int i, limit, k;

	k = us_city_in_state_beginning_index[state_indx];
	limit = us_cities_in_states_number[state_indx];

	out << "Beginning index for state " << us_states[state_indx] << " is "
			<< k << endl;
	out << "Number of cities is " << limit  << endl;
	for (i = 0; i < limit; i++) {
		out << "Check city with index " << us_cities_in_states[k+i] <<
			" and it should be city " << us_cities[us_cities_in_states[k+i]] << endl; 
		if (city_indx == us_cities_in_states[k+i])
			return 1;
	}
	return 0;
}

int ematch_class::check_if_state_in_region (int state_index, int region_index, ostream &out)
    {
	int deduction = 100;

	//out.println("In checkIfStateInRegion for state " +constStruct.usStates[stateIndex]+ " and " +
	//		"region " + constStruct.usRegions[regionIndex]);
	if (the_state_is_in_the_region(state_index, region_index,  out)) { 
		//out.println("SUCCESS: The state is in the region " + constStruct.usRegions[regionIndex]);
		deduction = 0;
	}
	return deduction;
    }

int ematch_class::check_if_city_in_state (int city_index, int state_index, ostream &out)
    {
	int deduction = 100;

	//out.println("In checkIfCityInState for city " +constStruct.usCities[cityIndex]+ " and " +
	//		"state " + constStruct.usStates[stateIndex]);
	if (the_city_is_in_the_state(city_index, state_index, /*ostream*/ out)) { 
		//out.println("SUCCESS: The city is in the state " + constStruct.usStates[stateIndex]);
		deduction = 0;
	}
	return deduction;
    }

int ematch_class::check_if_city_in_region (int city_index, int region_index, ostream &out)
    {
	int deduction = 100;
	int i, j;

	int r = us_state_in_region_beginning_index[region_index], s, l, st;

	//out.println("In checkIfCityInRegion for city " +constStruct.usCities[cityIndex]+ " and " +
	//		"region " + constStruct.usRegions[regionIndex] + ", beginning index=" + r);
	for (i=r; us_states_in_regions[i] != END_SUB_LIST; i++) {
		st = us_states_in_regions[i];
		s = us_city_in_state_beginning_index[st];
		l = us_cities_in_states_number[st];
		//out.println("i=" + i + ", s=" + s + ", l=" + l + ", st=" + st);
		//out.println("Check state " + constStruct.usStates[st]);
		for (j = 0; j < l; j++) {
			//out.println("Check city " + constStruct.usCities[constStruct.usCitiesInStates[j+s]] +
			//" with city index " + constStruct.usCitiesInStates[j+s]);
	        	if (the_city_is_in_the_state(city_index, st, out)) { 
				//out.println("SUCCESS: The city is in the state " +
				//		constStruct.usStates[st]);
				deduction = 0;
			}
		}
	}
	return deduction;
    }


/*
 *  Compute the rating based on the region information requested by a user.
 *  The parameter one_row contains a tuple retrieved from the job table that
 *		satisfies basic requirement. The one_row_ind is the corresponding
 *		indicate array.
 *  Value returned:  an integer between 0 and 100. 0 means perfect match,
 *		100 means no matching at all.  The method compute_a_job_rating()
 *		will deduct the returned value from its final rating.
 */
int ematch_class::compute_region_rating(mystring *one_row, int *one_row_ind, ostream &out)
{

	int  region_index=-1,  state_index=-1, city_index=-1, location_index=-1;

	int deduction = 100, tmp_deduction =-1;			// Assume not match by default
	int check_state_and_or_city_also = 0;

	mystring region_name, state_name, city_name, location_name;
	my_string_class my_string_instance;

	region_name = new char [JOB_TABLE_REGION_NAME_LENGTH];
	state_name  = new char [JOB_TABLE_STATE_NAME_LENGTH];
	city_name   = new char [JOB_TABLE_LOCATION_LENGTH];

	// Job search
	if (search_type == JOB_SEARCH) {
		if (one_row_ind[JOB_TABLE_REGION_NAME] >= 0) {
			strcpy (region_name, one_row[JOB_TABLE_REGION_NAME]); 
			my_string_instance.to_lower(region_name);
			region_index = find_region_index(region_name);
		}
		if (one_row_ind[JOB_TABLE_STATE_NAME] >= 0) {
			strcpy (state_name, one_row[JOB_TABLE_STATE_NAME]); 
			my_string_instance.to_lower(state_name);
			state_index = find_state_index(state_name);
		}
		if (one_row_ind[JOB_TABLE_LOCATION] >= 0) {
			strcpy (city_name, one_row[JOB_TABLE_LOCATION]); 
			my_string_instance.to_lower(city_name);
			city_index =find_city_index(city_name);
		}
		if (region_index != -1) {
			// perfect match, or asked region is contained in the job region
			if (region_compability[region_index][asked_location_index] == 1)
				deduction = 0;
			else if (region_compability[region_index][asked_location_index] == 2)
			{
			    deduction = 70;
			    if (state_index != -1)
			       tmp_deduction = check_if_state_in_region(state_index, asked_location_index, out);
			    else if (city_index != -1)
			       tmp_deduction = check_if_city_in_region(city_index, asked_location_index, out);

			    deduction = min(deduction, tmp_deduction);
			}
		} else if (state_index != -1) {
			deduction = check_if_state_in_region(state_index, asked_location_index, out);
		} else if (city_index != -1) {
			deduction = check_if_city_in_region(city_index, asked_location_index, out);
		}
	// Member search
	} else if (search_type == MEMBER_SEARCH) {
		if (one_row_ind[MEMBER_TABLE_DESIRED_JOB_LOCATION] >= 0) {
			location_name   = new char [MEMBER_TABLE_DESIRED_JOB_LOCATION_LENGTH];
			strcpy (location_name, one_row[MEMBER_TABLE_DESIRED_JOB_LOCATION]); 
			my_string_instance.to_lower(location_name);
			location_index = find_city_index(location_name);
			// Details to be filled
		}
	// C_G search
	} else if (search_type == C_G_SEARCH) {
		if (one_row_ind[C_G_TABLE_DESIRED_JOB_LOCATION] >= 0) {
			location_name   = new char [C_G_TABLE_DESIRED_JOB_LOCATION_LENGTH];
			strcpy (location_name, one_row[C_G_TABLE_DESIRED_JOB_LOCATION]); 
			my_string_instance.to_lower(location_name);
			location_index = find_city_index(location_name);
			// Details to be filled
		}
	} else {
		out << "Unknown Search Type!" << endl;
		deduction = 100;
	}

	return deduction;

} // End of compute_region_rating

/*
 *  Compute the rating based on the state information specified by a user.
 *  The parameter asked_state_index is the index of the state desired.
 *              Parameter one_row contains a tuple retrieved from the job table that
 *		satisfies basic requirement. The parameter one_row_ind is the corresponding
 *		indicate array.
 *  Value returned:  an integer between 0 and 100. 0 means perfect match,
 *		100 means no matching at all.  The method compute_a_job_rating()
 *		will deduct the returned value from its final rating.
 */
int ematch_class::compute_state_rating (int asked_state_index, mystring *one_row, int *one_row_ind, ostream &out)
{

	int i, j, k;

	my_string_class my_string_instance;

	int deduction = 100, tmp_deduction=100;

	int  region_index=-1, state_index=-1, city_index=-1, location_index=-1;
	mystring region_name, state_name, city_name, location_name;

	region_name = new char [JOB_TABLE_REGION_NAME_LENGTH];
	state_name  = new char [JOB_TABLE_STATE_NAME_LENGTH];
	city_name   = new char [JOB_TABLE_LOCATION_LENGTH];

	//out.println("Calling computeStateRating");
	if (search_type == JOB_SEARCH) {
		if (one_row_ind[JOB_TABLE_REGION_NAME] >= 0) {
			strcpy (region_name, one_row[JOB_TABLE_REGION_NAME]); 
			my_string_instance.to_lower(region_name);
			region_index = find_region_index(region_name);
		}
		if (one_row_ind[JOB_TABLE_STATE_NAME] >= 0) {
			strcpy (state_name, one_row[JOB_TABLE_STATE_NAME]); 
			my_string_instance.to_lower(state_name);
			state_index = find_state_index(state_name);
		}
		if (one_row_ind[JOB_TABLE_LOCATION] >= 0) {
			strcpy (city_name, one_row[JOB_TABLE_LOCATION]); 
			my_string_instance.to_lower(city_name);
			city_index =find_city_index(city_name);
		}

		if (state_index != -1) {

			//out.println("Asked state index is " + askedStateIndex);
			//out.println("Asked state name is " + constStruct.usStates[askedStateIndex]);

			j = neighbor_state_beginning_index[asked_state_index];
			k = us_neighbor_state_number[asked_state_index];

			//out.println( "beginning state index = " + j + " and # of neighbors is ");
			for (i = 0; i < 2*k; i=i+2) {
				//out.println ("Consider state with " + j+i +
				//	" as index in usNeighborStateRatingList and " +
				//	"[j+i]=" +  constStruct.usNeighborStateRatingList[j+i]);
				//out.println ("The state name should be " +
				//		constStruct.usStates[constStruct.usNeighborStateRatingList[j+i]]);

				if (us_neighbor_state_rating_list[j+i] == state_index) {
					deduction = us_neighbor_state_rating_list[j+i+1];
					break;
				}
			}
		} else if (city_index != -1) { // The row does not have a valid state, but has a valid city

			j = neighbor_state_beginning_index[asked_state_index];
			k = us_neighbor_state_number[asked_state_index];

			for (i = 0; i < 2*k; i+=2) {

				state_index = us_neighbor_state_rating_list[j+i];
				//out.println("Consider state with " + stateIndex +
				//" as index. The state name should be " + constStruct.usStates[stateIndex]);
				if (the_city_is_in_the_state(city_index, state_index, out)) { 
					//out.println("SUCCESS: The city is in the neighbor state "
					//		+ constStruct.usStates[stateIndex]);
					deduction = us_neighbor_state_rating_list[j+i+1];
					break;
				}
			}
		} else if (region_index != -1) { // The row does not have a valid state or city,
						 //    but does have a valid region name
			deduction = 30; // by default, the rating deduction is 30% for this case
			tmp_deduction = check_if_state_in_region(asked_state_index, region_index, out);
		        deduction = max(deduction, tmp_deduction);
		}
	// Member search
	} else if (search_type == MEMBER_SEARCH) {
		if (one_row_ind[MEMBER_TABLE_DESIRED_JOB_LOCATION] >= 0) {
			location_name   = new char [MEMBER_TABLE_DESIRED_JOB_LOCATION_LENGTH];
			strcpy (location_name, one_row[MEMBER_TABLE_DESIRED_JOB_LOCATION]); 
			my_string_instance.to_lower(location_name);
			location_index = find_city_index(location_name);
			// Details to be filled
		}
	// Member search
	} else {
		out << "Unknown Search Type!" << endl;
		deduction = 100;
	}

	return deduction;
    } // End of computeStateIndex


/*
 *  Compute the rating based on the city information specified by a user.
 *  The parameter asked_city_index is the index of the city desired.
 *              The parameter one_row contains a tuple retrieved from the job table that
 *		satisfies basic requirement. Parameter one_row_ind is the corresponding
 *		indicate array
 *  Value returned:  an integer between 0 and 100. 0 means perfect match,
 *		100 means no matching at all.  The method compute_a_job_rating()
 *		will deduct the returned value from its final rating.
 */
    int ematch_class::compute_city_rating(int asked_city_index, mystring * one_row,
		int * one_row_ind, ostream &out)
    {

	int deduction = 100;

	int i, j, k;
	int city_index;

	mystring city_name, asked_city_name;
	my_string_class my_string_instance;


	out << "askedCityIndex=" <<  asked_city_index << endl;

	k = max(JOB_TABLE_LOCATION_LENGTH, MEMBER_TABLE_DESIRED_JOB_LOCATION_LENGTH);
	j = max(k, C_G_TABLE_DESIRED_JOB_LOCATION_LENGTH);

	city_name = new char[j];
	asked_city_name = new char[j];

	if (search_type == JOB_SEARCH) {
	    if (one_row_ind[JOB_TABLE_LOCATION] < 0)
		return deduction;
	    else
		strcpy (city_name, one_row[JOB_TABLE_LOCATION]);
	} else if (search_type == MEMBER_SEARCH) {
	    if (one_row_ind[MEMBER_TABLE_DESIRED_JOB_LOCATION] < 0)
		return deduction;
	    else
		strcpy (city_name, one_row[MEMBER_TABLE_DESIRED_JOB_LOCATION]);
	} else if (search_type == C_G_SEARCH) {
	    if (one_row_ind[C_G_TABLE_DESIRED_JOB_LOCATION] < 0)
		return deduction;
	    else
		strcpy (city_name, one_row[C_G_TABLE_DESIRED_JOB_LOCATION]);
	} else {
		out << "Error: unknown search type." << endl;
		return -1;
	}

	//asked_city_index = find_city_index(asked);
	my_string_instance.to_lower(city_name);
	city_index = find_city_index(city_name);

	if (asked_city_index == city_index)
		return 0;

	j = neighbor_city_beginning_index[asked_city_index];

	k = us_neighbor_city_number[asked_city_index];

	out << "Considering if city " <<  city_name << " is a neighbor city of " << asked_city_name  << endl;
	out << "City " << asked_city_name << " has index " << asked_city_index <<
			" and has " << k << " neighbor cities"<< endl;
	//out.println("It should begin at position " + j + " in usNeighborCityRatingList");
	//out.println("City " + cityName + " has index " + cityIndex);

	for (i = 0; i < 2*k; i=i+2) {
		out << "Consider city with " << j<< "+" << i <<
					" as index in usNeighborCityRatingList and " <<
					"[j+i]=" << us_neighbor_city_rating_list[j+i] << endl;
		out << "The city name should be " <<
				us_cities[us_neighbor_city_rating_list[j+i]] << endl;

		if (us_neighbor_city_rating_list[j+i] == city_index) {
			deduction = us_neighbor_city_rating_list[j+i+1];
			break;
		}
	}

	return deduction;
    } // End of compute_city_rating()


    int ematch_class::compute_sal_rating (int sal)
    {    	
	int deduction = 0;
	float percent;


	if (asked_min_salary > sal)
	{
		percent = (((float)(asked_min_salary - sal)) / ((float)(asked_min_salary + 1)));
										
/*
		if (percent <= 0.05)		// salary is 95% or above
			deduction = 5;
		else if (percent <= 0.10)	// salary is between 90% and 95%
			deduction = 10;
		else if (percent <= 0.15)	// salary is between 85% and 90%
			deduction = 15;
		else if (percent <= 0.20)	// salary is between 80% and 85%
			deduction = 20;
		else if (percent <= 0.25)	// salary is between 75% and 80%
			deduction = 25;
		else if (percent <= 0.30)	// salary is between 70% and 75% 
			deduction = 30;
		else if (percent <= 0.35)	// salary is between 65% and 70%
			deduction = 35;
		else if (percent <= 0.40)	// salary is between 60% and 65%
			deduction = 40;
		else if (percent <= 0.45)	// salary is between 55% and 60%
			deduction = 45;
		else if (percent <= 0.50)	// salary is between 50% and 55%
			deduction = 50;
		else if (percent <= 0.55)	// salary is between 45% and 50%
			deduction = 55;
		else if (percent <= 0.60)	// salary is between 40% and 45%
			deduction = 60;
		else if (percent <= 0.65)	// salary is between 35% and 40%
			deduction = 65;
		else deduction = 70;		// salary is at most 35%
*/
		deduction = percent * 100;
	}
	return deduction;
    }


/*
 *
 */
int ematch_class::find_region_index(mystring a_name)
{
	int i;

	if (country_code == USA)
		for (i = 0; i < NUMBER_OF_US_REGIONS; i++)
			if (strcmp (a_name, us_regions[i]) == 0)
				return i;
	return -1;

}

int ematch_class::find_state_index(mystring a_name)
{
	int i;

	if (country_code == USA)
		for (i = 0; i < NUMBER_OF_US_STATES; i++)
			if (strcmp (a_name, us_states[i]) == 0)
				return i;
	return -1;

}


int ematch_class::find_city_index(mystring a_name)
{
	int i;


	if (country_code == USA)
		for (i = 0; i < NUMBER_OF_US_CITIES; i++)
			if (strcmp (a_name, us_cities[i]) == 0)
				return i;
	return -1;

}

/*
 * Compute the rating for a tuple that satisfies the priliminary
 *	condition formed by the prepare_a_job_search_query() method
 *      in the file ematch.pc.
 * Depending upon the specified information submitted by a user,
 *  this method may invoke compute_region_rating(), compute_state_rating(),
 *	compute_city_rating(), and compute_sal_rating().
 * Value returned: the rating of the tuple. A negative rating implies that
 *      the tuple is not qualified for final output.
 */
    int ematch_class::compute_a_job_rating (mystring *one_row, int *one_row_ind, ostream &out)
    {    	
	int tmp_rating = 100;
	int i;
	int sal;

	//out.println("Consider column 1 with paraValues[1]="+paraValues[1]);
	//out.println("Consider column 8 with paraValues[8]="+paraValues[8]);
	//out.println("constStruct.COLUMN_NUMBER_IN_JOB_TABLE="+constStruct.COLUMN_NUMBER_IN_JOB_TABLE);
	//out.println("locationSearchType = " + locationSearchType);
	for (i = 0; i < COLUMN_NUMBER_IN_JOB_TABLE; i++)
	{
		if (column_listed[i] && !(value[i] == "All") && !(value[i] == "Any"))  {
		//out.println("CONSIDER column i="+i+" paraValues[i]="+paraValues[i] + "---");
		/* Search by region */
			if ((i==JOB_TABLE_REGION_NAME ) && (location_search_type==SEARCH_BY_REGION))
			{
				tmp_rating -= compute_region_rating(one_row, one_row_ind, out);
			} /* Search by state */
			else if ((i==JOB_TABLE_STATE_NAME ) &&
				(location_search_type==SEARCH_BY_STATE))
			{
				tmp_rating -= compute_state_rating(asked_location_index, one_row, one_row_ind, out);
			} /* Search by city */
			else if ((i==JOB_TABLE_LOCATION) && (location_search_type==SEARCH_BY_CITY))
			{
				tmp_rating -= compute_city_rating(asked_location_index, one_row,
								one_row_ind, out);
			} // salary
			else  if ((i==JOB_TABLE_MIN_SALARY) && (asked_min_salary != 0) && (one_row_ind[i] >= 0))
			{
				sal = atoi(one_row[i]);
				//out.println("Check salary for row " + i + " with sal = " + sal);
				tmp_rating -= compute_sal_rating(sal);
			}

			// un-qualified job entry
			if (tmp_rating <= 0)
				break;
		}
	}

	return tmp_rating;
    }	


/*
 * Insert a matched rwo (rating > 0)
 */
void ematch_class::insert_a_matched_row(ostream &out, mystring *one_row, 
						int *one_row_ind, int a_rating)
{

	int i, str_len;

	out << " Insert a selected row " << total_matched_rows <<
			" with rating " << a_rating << " column num=" << column_number <<endl;

	for (i = 0; i < column_number; i++) {

		out << " Process row " << i+1 << " " << one_row[i] << endl;
		str_len = strlen(one_row[i]);

		result_array[total_matched_rows][i] = new char [str_len+1];
		strcpy (result_array[total_matched_rows][i], one_row[i]);

		result_array_ind[total_matched_rows][i] = (int) one_row_ind[i];

		if (output_width[i] < str_len)
			output_width[i] = str_len;

	}

	ratings[total_matched_rows] = a_rating;

	total_matched_rows++;


}

void ematch_class::print_neighbor_cities (ostream &out)
{

	int b, i, j, k;


	for (i = 0; i< NUMBER_OF_US_CITIES; i++) {
			b = neighbor_city_beginning_index[i];

			k = us_neighbor_city_number[i];

			out << "C_CITY " << i << " is " << us_cities[i] << " and has " << 
					b << " as index, has " << k << " neighbor cities:" << endl;

			for (j = 0; j < 2*k; j=j+2)  
				out << us_cities[us_neighbor_city_rating_list[b+j]] << ",";
			out << endl;

	}

}


void ematch_class::print_neighbor_states (ostream &out)
{

	int b, i, j, k;


	for (i = 0; i< NUMBER_OF_US_STATES; i++) {

			b = neighbor_state_beginning_index[i];

			k = us_neighbor_state_number[i];

			out << "S_STATE " << i << " is " << us_states[i] << " and has " << 
					b << " as index, has "  << k << " neighbor states:" << endl;


			for (j = 0; j < 2*k; j=j+2)  
				out << us_states[us_neighbor_state_rating_list[b+j]] << ",";
			out << endl;

	}

}


void ematch_class::print_cities_in_states (ostream &out)
{

	int b, i, j, k;


	for (i = 0; i< NUMBER_OF_US_STATES; i++) {
			b = us_city_in_state_beginning_index[i];


			k = us_cities_in_states_number[i];

			for (j = 0; j < k; j++)
				if (us_cities_in_states[b+j] >= 0)
					out << us_cities[us_cities_in_states[b+j]] << ",";
				else 
					out << "NONE";
			out << endl;

	}

}

void ematch_class::print_states_in_regions (ostream &out)
{

	int b, i, j, k;


	for (i = 0; i< NUMBER_OF_US_REGIONS; i++) {

			b = us_state_in_region_beginning_index[i];


			k = us_cities_in_states_number[i];

			out << "STTATES IN REGIONS -- REGION " << i << " is " <<
					us_regions[i] << " and has " << 
					b << " as start index, and its states are:" << endl;

			for (j = 0; us_states_in_regions[b+j] >= 0; j++)
					out << us_states[us_states_in_regions[b+j]] << ",";
			out << " with a total " << j << " states";
			out << endl;

	}

}


/*
 *
 *
 *  Created:    08/05/2000
 *
 *  Modified:   08/08/2000
 *              01/12/2002
 */




void ematch_class::set_initial_job_environ(int table_indx, int my_search_typ, int country_cod)
{
	//cout << "Initialize first enviroment of ematch_class with "<< table_indx
	//			<< " and country_code = " << country_cod << endl;

	country_code = country_cod;

	set_initial_environ(my_search_typ, table_indx, country_cod);

	job_type_required = 0;
	job_title_required = 0;
	my_search_type = JOB_SEARCH;

	specialization_required = 0;
	country_code_required = 0;

	region_name_required = 0;
	state_name_required = 0;
	city_name_required = 0;

	min_salary_required = 0;
	max_salary_required = 0;

	company_name_required = 0;

	start_date_required = 0;
}

/*
 * This method separates each pair of the form
 * 'name=value' in an array to two array, an name array
 * and a value array, both defined in a ematch_class  
 * instance.
 *
 * It is assumed there are no space characters around
 * 'name' or 'value'
 *
 */
void ematch_class::separate_each_job_pair (ostream &out)

{
	int i, j, m, old_j;
	int k, str_len, pair_len;

	mystring n, v;
	int actual_pair_number = 0;
	my_string_class my_string_instance;

	out << "BBEGINNING of separate_each_job_pair\n";

	str_len = strlen(cgi_string);


	asked_min_salary = asked_max_salary = 0;

	n = new char[str_len];
	v = new char[str_len];

	old_j = -1;

	for (i = 0, j=0; i < pair_number; i++) {


		pair_len = strlen(cgi_string_pairs[i]);

		v = strchr(cgi_string_pairs[i], '=');


		k = strlen(v);


		if (j > old_j) {
			name[j]  = new char[pair_len - k + 1];
			value[j] = new char[2*k];
			unchanged_value[j] = new char[2*k];
		}

		old_j = j;

		strncpy(name[j],  cgi_string_pairs[i], pair_len-k);
		strncpy(value[j], v+1, k-1);
		strncpy(unchanged_value[j], v+1, k-1);

		(name[j])[pair_len-k] = '\0';
		(value[j])[k-1] = '\0';
		(unchanged_value[j])[k-1] = '\0';

		convert_a_single_quote_and_percent_sign(value[j]);

		my_string_instance.to_lower(name[j]);  // Convert every char to lower case

		if (ematch_or_insert == EMATCH_)					// Ematch call
			my_string_instance.to_lower(value[j]);  // Convert to lower case

		out << "name=" << name[j] << " and value = " << value[j] << endl;

		// By-pass name=All, Any pair
		if ((strcmp(value[j], "All") == 0) || (strcmp(value[j], "all") == 0) ||
			(strcmp(value[j], "Any") == 0) || (strcmp(value[j], "any") == 0))
			continue;

		convert_a_job_table_column_name(name[j]);

		m = find_job_table_column_index(name[j]);
		if (m < 0) {
			out << "Invalid column name: " << name[j] << endl;
			exit (-1);
		} else
			out << "Column name: " << name[j] << ", index m = " << m << endl;

		column_listed[m] = 1;
		name_index[m] = j;
		name_to_column_index[j] = m;

		if (m == JOB_TABLE_JOB_TYPE) {

			job_type_required = 1;
			asked_job_type = new char [JOB_TABLE_JOB_TYPE_LENGTH];
			strcpy(asked_job_type, value[j]);

		} else if (m == JOB_TABLE_JOB_TITLE) {

			job_title_required = 1;
			asked_job_title = new char [JOB_TABLE_JOB_TITLE_LENGTH];
			strcpy(asked_job_title, value[j]);

		} else if (m == JOB_TABLE_SPECIALIZATION) {

			specialization_required = 1;
			asked_specialization = new char [JOB_TABLE_SPECIALIZATION_LENGTH];
			strcpy(asked_specialization, value[j]);

		} else if (m == JOB_TABLE_COUNTRY_CODE) {

			if (!my_string_instance.is_digit(value[j])) {
				out << "Invalid country code field!" << endl;
			} else {
				country_code = atoi(value[j]);
				country_code_required = 1;
			}

		} else if (m == JOB_TABLE_REGION_NAME) {

			region_name_required = 1;
			asked_region_name = new char [JOB_TABLE_REGION_NAME_LENGTH];
			strcpy(asked_region_name, value[j]);

		} else if (m == JOB_TABLE_STATE_NAME) {

			state_name_required = 1;
			asked_state_name = new char [JOB_TABLE_STATE_NAME_LENGTH];
			strcpy(asked_state_name, value[j]);

		} else if (m == JOB_TABLE_CITY) {

			city_name_required = 1;
			asked_city_name = new char [JOB_TABLE_CITY_LENGTH];
			strcpy(asked_city_name, value[j]);

		} else if (m == JOB_TABLE_MIN_SALARY) {
			out << "Now converting  asked_min_salary " << value[j] << endl;

			if (!my_string_instance.is_digit(value[j])) {
				out << "Invalid min salary field!" << endl;
			} else {
				asked_min_salary = atoi(value[j]);
				min_salary_required = 1;
			}

		} else if (m == JOB_TABLE_MAX_SALARY) {

			if (!my_string_instance.is_digit(value[j])) {
				out << "Invalid max salary field!" << endl;
			} else {
				asked_max_salary = atoi(value[j]);
				max_salary_required = 1;
			}


		} else if (m == JOB_TABLE_COMPANY_NAME) {

			company_name_required = 1;
			asked_company_name = new char [JOB_TABLE_COMPANY_NAME_LENGTH];
			strcpy(asked_company_name, value[j]);
		}

		out << "COLUMN " << m << " with name " << name[j] << " at position "
					<< j << " listed" << endl;
		j++;
	}

	pair_number = j;
	out << "min_salary_required = " << min_salary_required << endl;
	out << " Returning from separate_each_job_pair with pair_number=" << pair_number << "\n";


} // ematch_class::separate_each_job_pair ()


int ematch_class::validate_job_table_column_names(void)
{
	int i, j, k;
	int flag;
	int total_invalid=0;
		

	for (i=0; i < pair_number; i++) {
		flag = 1;

		for (j = 0; j < COLUMN_NUMBER_IN_JOB_TABLE; j++) {

			if ( !strcmp(name[i], job_table_column_names[j])) {
				flag = 0;
				break;
			}
			else {

				k = find_column_index(name[i]);
				if (k >= 0 ) flag = 0;
			
			}
		}

		if (flag) {
			cout << "Invalid column name: " << name[i] << endl;
			total_invalid++;
		}
	}
	if (total_invalid > 0) {
		cout << "Total " << total_invalid << " column names!\n";
		return(-total_invalid);
	}
	return(0);
} /* end of  ematch_class::validate_job_table_column_names(void) */

int ematch_class::find_job_table_column_index(mystring a_name)
{
	int i = 0;


	for (i = 0; i < column_number; i++) {

		if (strcmp (a_name, job_table_column_names[i]) == 0)
			return i;
	}
	return -1;

} /* end of ematch_class::find_job_table_column_index(mystring) */

//
// Microsoft C++ provides two function min and max with different meaning.
// Therefore I have to write these two for convenience
//
int ematch_class::max(int a, int b)
{
	if (a >= b)
		return a;
	else
		return b;
}

int ematch_class::min(int a, int b)
{
	if (a <= b)
		return a;
	else
		return b;
}
