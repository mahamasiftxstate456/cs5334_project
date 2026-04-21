
/*
 *  Created:  01/15/2002
 *  Modified: 03/31/2002
 */


/*#include "my_c_cpp_includes.h"
#include "c_cpp_header.h"*/

#include "my_string_class.h"

#define COLUMN_NUMBER_IN_JOB_TABLE 14

//
//  It will extract each substring of the form 'a=b' in a CGI parameter
//  to the public variable cgi_string_pairs in class cgi_string_class
//
//  Before calling the function, the function  find_pair_number() must
//  be called first. That function will find the number of pairs and
//  will also allocate space to the variable cgi_string_pairs
//
void my_string_class::reverse_string (mystring result,  mystring source, int len)
{
	int i;
	for (i = 0; i < len; i++) {
		result[i] = source[len-i-1];
	}
}

// To get rid of the padding blank charcters in varchar2 type columns
// that are fectured into C++ char string variables.
void my_string_class::get_rid_of_padding_blanks_2 (mystring result, mystring source, int len)
{

     char *temp_str;

     int i, j;

	 temp_str = new char [len];

	 // reverse_string (temp_str, source);

	 temp_str = strchr(source, ' ');
	 i = strlen(source)-strlen(temp_str);
	 strncpy (result, source, i);

	 result[i] = '\0';

}

// To get rid of the padding blank charcters in varchar2 type columns
// that are fectured into C++ char string variables.
void my_string_class::get_rid_of_padding_blanks (mystring result, mystring source, int len)
{

     //char *temp_str;

     int i, j;

	 // temp_str = new char [len];

	 // reverse_string (temp_str, source);

	 for (i=len-1, j=0; i > 0 ; i--, j++)
			if (source[i] != ' ') break;

	 strncpy (result, source, len-j);

	 result[len-j] = '\0';

}

// To get rid of the padding blank charcters in normal C/C++ character string
// variable. The parameter str should point to a storage area of at least
// strlen(str) + 1 characters
// 
void my_string_class::remove_trailing_space_chars (mystring str)
{

	int i;
	int len;

	len = strlen(str);

	for (i=len-1; i >= 0; i--)
		if ((str[i] != ' ') && (str[i] != '\t')) break;


	str[i+1] = '\0';
}

/*
 * Return 1 if the given char string is an all-blank char string;
 *        0 otherwise.
 */
int my_string_class::is_a_blank_string (mystring s)
{
     int i, j;

	 // temp_str = new char [len];

	 // reverse_string (temp_str, source);

	 j = strlen(s);

	 for (i=0; i < j; i++)
			if ((s[i] != ' ') && (s[i] != '\t')) return 0;

	return 1;
}

/*
 * Return 1 if the given char string contains all digit letters;
 *        0 otherwise.
 */
int my_string_class::is_digit (mystring s)
{
     int i, j;

	 // temp_str = new char [len];

	 // reverse_string (temp_str, source);

	 j = strlen(s);

	 for (i=0; i < j; i++)
			if ((s[i] < '0') || (s[i] > '9')) return 0;

	return 1;
}


void my_string_class::to_lower (mystring s)
{
     int i, j;

	 // temp_str = new char [len];

	 // reverse_string (temp_str, source);

	 j = strlen(s);

	 for (i=0; i < j; i++)
			s[i] = tolower(s[i]);
}

void my_string_class::to_upper (mystring s)
{
     int i, j;

	 // temp_str = new char [len];

	 // reverse_string (temp_str, source);

	 j = strlen(s);

	 for (i=0; i < j; i++)
			s[i] = toupper(s[i]);
}
