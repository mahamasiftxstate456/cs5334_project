
/* Result Sets Interface */
#ifndef SQL_CRSR
#  define SQL_CRSR
  struct sql_cursor
  {
    unsigned int curocn;
    void *ptr1;
    void *ptr2;
    unsigned int magic;
  };
  typedef struct sql_cursor sql_cursor;
  typedef struct sql_cursor SQL_CURSOR;
#endif /* SQL_CRSR */

/* Thread Safety */
typedef void * sql_context;
typedef void * SQL_CONTEXT;

/* Object support */
struct sqltvn
{
  unsigned char *tvnvsn; 
  unsigned short tvnvsnl; 
  unsigned char *tvnnm;
  unsigned short tvnnml; 
  unsigned char *tvnsnm;
  unsigned short tvnsnml;
};
typedef struct sqltvn sqltvn;

struct sqladts
{
  unsigned int adtvsn; 
  unsigned short adtmode; 
  unsigned short adtnum;  
  sqltvn adttvn[1];       
};
typedef struct sqladts sqladts;

static struct sqladts sqladt = {
  1,1,0,
};

/* Binding to PL/SQL Records */
struct sqltdss
{
  unsigned int tdsvsn; 
  unsigned short tdsnum; 
  unsigned char *tdsval[1]; 
};
typedef struct sqltdss sqltdss;
static struct sqltdss sqltds =
{
  1,
  0,
};

/* File name & Package Name */
struct sqlcxp
{
  unsigned short fillen;
           char  filnam[14];
};
static const struct sqlcxp sqlfpn =
{
    13,
    "ematch_job.pc"
};


static unsigned int sqlctx = 586907;


static struct sqlexd {
   unsigned long  sqlvsn;
   unsigned int   arrsiz;
   unsigned int   iters;
   unsigned int   offset;
   unsigned short selerr;
   unsigned short sqlety;
   unsigned int   occurs;
      const short *cud;
   unsigned char  *sqlest;
      const char  *stmt;
   sqladts *sqladtp;
   sqltdss *sqltdsp;
   unsigned char  **sqphsv;
   unsigned long  *sqphsl;
            int   *sqphss;
            short **sqpind;
            int   *sqpins;
   unsigned long  *sqparm;
   unsigned long  **sqparc;
   unsigned short  *sqpadto;
   unsigned short  *sqptdso;
   unsigned int   sqlcmax;
   unsigned int   sqlcmin;
   unsigned int   sqlcincr;
   unsigned int   sqlctimeout;
   unsigned int   sqlcnowait;
            int   sqfoff;
   unsigned int   sqcmod;
   unsigned int   sqfmod;
   unsigned int   sqlpfmem;
   unsigned char  *sqhstv[4];
   unsigned long  sqhstl[4];
            int   sqhsts[4];
            short *sqindv[4];
            int   sqinds[4];
   unsigned long  sqharm[4];
   unsigned long  *sqharc[4];
   unsigned short  sqadto[4];
   unsigned short  sqtdso[4];
} sqlstm = {13,4};

// Prototypes
extern "C" {
  void sqlcxt (void **, unsigned int *,
               struct sqlexd *, const struct sqlcxp *);
  void sqlcx2t(void **, unsigned int *,
               struct sqlexd *, const struct sqlcxp *);
  void sqlbuft(void **, char *);
  void sqlgs2t(void **, char *);
  void sqlorat(void **, unsigned int *, void *);
}

// Forms Interface
static const int IAPSUCC = 0;
static const int IAPFAIL = 1403;
static const int IAPFTL  = 535;
extern "C" { void sqliem(unsigned char *, signed int *); }

typedef struct { unsigned short len; unsigned char arr[1]; } VARCHAR;
typedef struct { unsigned short len; unsigned char arr[1]; } varchar;

/* cud (compilation unit data) array */
static const short sqlcud0[] =
{13,4130,1,0,0,
5,0,0,0,0,0,539,203,0,0,4,4,0,1,0,1,97,0,0,1,10,0,0,1,10,0,0,1,10,0,0,
36,0,0,2,0,0,529,222,0,0,1,1,0,1,0,1,5,0,0,
55,0,0,2,0,0,523,229,0,0,1,1,0,1,0,1,32,0,0,
74,0,0,2,0,0,527,272,0,0,0,0,0,1,0,
89,0,0,3,0,0,542,275,0,0,0,0,0,1,0,
104,0,0,2,0,0,526,491,0,0,1,0,0,1,0,2,32,0,0,
123,0,0,4,0,0,544,771,0,0,0,0,0,1,0,
138,0,0,2,0,0,531,852,0,0,1,1,0,1,0,3,32,0,0,
157,0,0,2,0,0,532,941,0,0,1,1,0,1,0,3,32,0,0,
};



/*
 *  
 *
 *  Search the Ematch database. Dynamic SQL method 3/4 is used to
 *  have maximum flexibility
 * 
 *  Two parameters are required. For both job and member search, the
 *  first parameter is a CGI string of the form "name=value&...".
 *  The second parameter indicates search type:
 *
 *		1, 2 for job search
 *
 *  Tables searched:  job
 *
 *
 *  Created:    02/03/2000
 *
 *  Modified:   02/08/2000
 *		02/14/2000
 *		03/10/2000
 *		03/14/2000
 *		03/31/2000
 *		04/13/2000
 *		04/21/2000
 *		06/23/2000
 *		07/22/2000
 *		08/01/2000
 *		08/05/2001
 *		01/12/2002
 *		03/12/2003
 *		02/01/2004
 *		02/20/2005

 *		03/27/2008
 *		03/17/2012
 *		03/30/2017: change of "CONNECT" syntax
 *
 *              03/20/2023: ISO char* to [] string change
 */


#include <stdio.h>
#include <string.h>
#include <time.h>


#include "local_const.h"
#include "ematch_class.h"

//#include "ematch_const_struct.h"

#include <sqlda.h>
#include <sqlcpr.h>

/* Include the SQL Communications Area, a structure through
 * which ORACLE makes runtime status information such as error
 * codes, warning flags, and diagnostic text available to the
 * program.
 */
#include <sqlca.h>

/* Include the ORACLE Communications Area, a structure through
 * which ORACLE makes additional runtime status information
 * available to the program.
 */
#include <oraca.h>

/* The ORACA=YES option must be specified to enable you
 * to use the ORACA.
 */

/* EXEC ORACLE OPTION (ORACA=YES); */ 

//EXEC ORACLE OPTION (CHAR_MAP=VARCHAR2);

/* Specifying the RELEASE_CURSOR=YES option instructs Pro*C
 * to release resources associated with embedded SQL
 * statements after they are executed.  This ensures that
 * ORACLE does not keep parse locks on tables after data
 * manipulation operations, so that subsequent data definition
 * operations on those tables do not result in a parse-lock
 * error.
 */

/* EXEC ORACLE OPTION (RELEASE_CURSOR=YES); */ 


/* EXEC SQL INCLUDE sqlda;
 */ 
/*
 * $Header: precomp/public/sqlda.h /main/11 2020/07/19 18:54:58 dgoddard Exp $ sqlda.h 
 */

/***************************************************************
*      The SQLDA descriptor definition                         *
*--------------------------------------------------------------*
*      VAX/3B Version                                          *
*                                                              *
* Copyright (c) 1987, 2011, Oracle and/or its affiliates. All rights reserved. 
***************************************************************/


/* NOTES
  **************************************************************
  ***                                                        ***
  *** This file is SOSD.  Porters must change the data types ***
  *** appropriately on their platform.  See notes/pcport.doc ***
  *** for more information.                                  ***
  ***                                                        ***
  **************************************************************
*/

/*  MODIFIED
    ardesai    07/15/10  - Bug[9491931]As we refer to sqlaldt, so include
                           sqlcpr.h
    ardesai    05/08/07  - Bug[6037057] Undef Y
    apopat     05/08/02  - [2362423] MVS PE to make lines shorter than 79
    apopat     07/31/99 -  [707588] TAB to blanks for OCCS
    lvbcheng   10/27/98 -  change long to int for sqlda
    lvbcheng   08/15/97 -  Move sqlda protos to sqlcpr.h
    lvbcheng   06/25/97 -  Move sqlda protos to this file
    jbasu      01/29/95 -  correct typo
    jbasu      01/27/95 -  correct comment - ub2->sb2
    jbasu      12/12/94 - Bug 217878: note this is an SOSD file
    Morse      12/01/87 - undef L and S for v6 include files
    Richey     07/13/87 - change int defs to long 
    Clare      09/13/84 - Port: Ch types to match SQLLIB structs
    Clare      10/02/86 - Add ifndef SQLDA
*/
#ifndef SQLDA_
#define SQLDA_ 1
 
#ifndef LINT
#ifndef ORA_PROC 
#ifndef SQLPRO
#  include <sqlcpr.h>
#endif /* SQLPRO */
#endif /* #ifndef ORA_PROC  */
#endif

#ifdef T
# undef T
#endif
#ifdef F
# undef F
#endif

#ifdef S
# undef S
#endif
#ifdef L
# undef L
#endif

#ifdef Y
 # undef Y
#endif
 
struct SQLDA {
  /* ub4    */ int        N; /* Descriptor size in number of entries        */
  /* text** */ char     **V; /* Ptr to Arr of addresses of main variables   */
  /* ub4*   */ int       *L; /* Ptr to Arr of lengths of buffers            */
  /* sb2*   */ short     *T; /* Ptr to Arr of types of buffers              */
  /* sb2**  */ short    **I; /* Ptr to Arr of addresses of indicator vars   */
  /* sb4    */ int        F; /* Number of variables found by DESCRIBE       */
  /* text** */ char     **S; /* Ptr to Arr of variable name pointers        */
  /* ub2*   */ short     *M; /* Ptr to Arr of max lengths of var. names     */
  /* ub2*   */ short     *C; /* Ptr to Arr of current lengths of var. names */
  /* text** */ char     **X; /* Ptr to Arr of ind. var. name pointers       */
  /* ub2*   */ short     *Y; /* Ptr to Arr of max lengths of ind. var. names*/
  /* ub2*   */ short     *Z; /* Ptr to Arr of cur lengths of ind. var. names*/
  /* ub8*   */ long long *CP; /* Ptr to Arr of column properties            */
  };
 
typedef struct SQLDA SQLDA;
 
#endif

/* ----------------- */
/* defines for sqlda */
/* ----------------- */

#define SQLSQLDAAlloc(arg1, arg2, arg3, arg4) sqlaldt(arg1, arg2, arg3, arg4) 

#define SQLSQLDAFree(arg1, arg2) sqlclut(arg1, arg2) 




/* EXEC SQL INCLUDE sqlca;
 */ 
/*
 * $Header: sqlca.h 24-apr-2003.12:50:58 mkandarp Exp $ sqlca.h 
 */

/* Copyright (c) 1985, 2003, Oracle Corporation.  All rights reserved.  */
 
/*
NAME
  SQLCA : SQL Communications Area.
FUNCTION
  Contains no code. Oracle fills in the SQLCA with status info
  during the execution of a SQL stmt.
NOTES
  **************************************************************
  ***                                                        ***
  *** This file is SOSD.  Porters must change the data types ***
  *** appropriately on their platform.  See notes/pcport.doc ***
  *** for more information.                                  ***
  ***                                                        ***
  **************************************************************

  If the symbol SQLCA_STORAGE_CLASS is defined, then the SQLCA
  will be defined to have this storage class. For example:
 
    #define SQLCA_STORAGE_CLASS extern
 
  will define the SQLCA as an extern.
 
  If the symbol SQLCA_INIT is defined, then the SQLCA will be
  statically initialized. Although this is not necessary in order
  to use the SQLCA, it is a good pgming practice not to have
  unitialized variables. However, some C compilers/OS's don't
  allow automatic variables to be init'd in this manner. Therefore,
  if you are INCLUDE'ing the SQLCA in a place where it would be
  an automatic AND your C compiler/OS doesn't allow this style
  of initialization, then SQLCA_INIT should be left undefined --
  all others can define SQLCA_INIT if they wish.

  If the symbol SQLCA_NONE is defined, then the SQLCA variable will
  not be defined at all.  The symbol SQLCA_NONE should not be defined
  in source modules that have embedded SQL.  However, source modules
  that have no embedded SQL, but need to manipulate a sqlca struct
  passed in as a parameter, can set the SQLCA_NONE symbol to avoid
  creation of an extraneous sqlca variable.
 
MODIFIED
    lvbcheng   07/31/98 -  long to int
    jbasu      12/12/94 -  Bug 217878: note this is an SOSD file
    losborne   08/11/92 -  No sqlca var if SQLCA_NONE macro set 
  Clare      12/06/84 - Ch SQLCA to not be an extern.
  Clare      10/21/85 - Add initialization.
  Bradbury   01/05/86 - Only initialize when SQLCA_INIT set
  Clare      06/12/86 - Add SQLCA_STORAGE_CLASS option.
*/
 
#ifndef SQLCA
#define SQLCA 1
 
struct   sqlca
         {
         /* ub1 */ char    sqlcaid[8];
         /* b4  */ int     sqlabc;
         /* b4  */ int     sqlcode;
         struct
           {
           /* ub2 */ unsigned short sqlerrml;
           /* ub1 */ char           sqlerrmc[70];
           } sqlerrm;
         /* ub1 */ char    sqlerrp[8];
         /* b4  */ int     sqlerrd[6];
         /* ub1 */ char    sqlwarn[8];
         /* ub1 */ char    sqlext[8];
         };

#ifndef SQLCA_NONE 
#ifdef   SQLCA_STORAGE_CLASS
SQLCA_STORAGE_CLASS struct sqlca sqlca
#else
         struct sqlca sqlca
#endif
 
#ifdef  SQLCA_INIT
         = {
         {'S', 'Q', 'L', 'C', 'A', ' ', ' ', ' '},
         sizeof(struct sqlca),
         0,
         { 0, {0}},
         {'N', 'O', 'T', ' ', 'S', 'E', 'T', ' '},
         {0, 0, 0, 0, 0, 0},
         {0, 0, 0, 0, 0, 0, 0, 0},
         {0, 0, 0, 0, 0, 0, 0, 0}
         }
#endif
         ;
#endif
 
#endif
 
/* end SQLCA */


SQLDA *bind_dp;
SQLDA *select_dp;

extern SQLDA *sqlald();
//extern SQLDA *SQLSQLDAAlloc();
extern void sqlnul();

varchar  table_name[MAX_TABLE_NAME_LENGTH];

/* exec sql begin declare section; */ 


// A structure to hold a tuple from the 'JOB' table

//char	*username = USERNAME; // These two should be defined in "local_const.h"
//char	*password = PASSWORD;

char    dynamic_stmt[4000];
/* EXEC SQL VAR dynamic_stmt IS STRING(4000); */ 


/* exec sql end declare section; */ 


void sql_error(void);
int alloc_descriptors(int, int, int);
int set_bind_variables(ofstream &);
int pre_retrieval(ofstream &);

int prepare_a_job_search_query (char [], ematch_class);

int retrieve_matched_job_rows(ematch_class);


int num_of_matched_rows = 0;

char debug_out_file_name[30] = "ematch_job_debug_out.txt";
char result_out_file_name[30] = "ematch_job_out.txt";

ofstream debug_out_stream;
ofstream result_out_stream;


/*
 *  The argv[1] is assumed to contain the CGI string submitted
 *  by a user to search the job database.
 *
 *  The argv[2] is optional. It is an integer. If it is 1, the
 *     search is approximate. If it is 2, the search is exact.
*/
int main(int argc, char * argv[])
{

	//char	specialization[SPECIALIZATION_LENGTH];
	/* exec sql begin declare section; */ 


		//char	*username = USERNAME; // These two should be defined in "local_const.h"
		//char	*password = PASSWORD;	
		char	oracle_credential[100];
   	/* exec sql end declare section; */ 

	strcpy (oracle_credential, ORACLE_CREDENTIAL);	
	
	char copy_output_file[100];

	int pair_number;			// Number of user info pieces

	int search_type = 1;			// 1, 2: job search;
						// 3, 4: member search;
						// 5, 6: new college graduate search.

	int my_search_type = 1; // set to 1 if job search; 2 if member_search; 3 new c_g search
	int my_table_index;

	int by_country_region_state_city = 0;
	int i, j;

	ematch_class my_job_instance(0); // 0=EMATCH (defined in local_const.h)

	debug_out_stream.open(debug_out_file_name);
	result_out_stream.open(result_out_file_name);

	// Call sql_error() function on any error in an embedded SQL statement.
	//
	/* EXEC SQL WHENEVER SQLERROR DO sql_error(); */ 


	/* Save text of current SQL statement in the ORACA if an error occurs.
	*/
	oraca.orastxtf = ORASTFERR;

	if (argc >= 3) 
		   search_type = atoi(argv[2]);

	debug_out_stream << "search_type = " << search_type << endl;

	my_search_type = JOB_SEARCH;
	my_table_index = JOB_TABLE_INDEX;

	my_job_instance.set_initial_job_environ(my_table_index,
				my_search_type,  USA);


	// extract name=value pairs
	my_job_instance.extract_cgi_pairs(debug_out_stream, argv[1]);
	my_job_instance.separate_each_job_pair(debug_out_stream);

	if (my_job_instance.validate_job_table_column_names() < 0)
		exit(-1);


	pair_number = my_job_instance.pair_number;

	debug_out_stream  << endl;
	debug_out_stream  << "Trying to connect as " << oracle_credential << endl;

	//EXEC SQL CONNECT :username IDENTIFIED BY :password;
	/* EXEC SQL CONNECT :oracle_credential; */ 

{
 struct sqlexd sqlstm;
 sqlorat((void **)0, &sqlctx, &oraca);
 sqlstm.sqlvsn = 13;
 sqlstm.arrsiz = 4;
 sqlstm.sqladtp = &sqladt;
 sqlstm.sqltdsp = &sqltds;
 sqlstm.iters = (unsigned int  )10;
 sqlstm.offset = (unsigned int  )5;
 sqlstm.cud = sqlcud0;
 sqlstm.sqlest = (unsigned char  *)&sqlca;
 sqlstm.sqlety = (unsigned short)4352;
 sqlstm.occurs = (unsigned int  )0;
 sqlstm.sqhstv[0] = (unsigned char  *)oracle_credential;
 sqlstm.sqhstl[0] = (unsigned long )100;
 sqlstm.sqhsts[0] = (         int  )100;
 sqlstm.sqindv[0] = (         short *)0;
 sqlstm.sqinds[0] = (         int  )0;
 sqlstm.sqharm[0] = (unsigned long )0;
 sqlstm.sqadto[0] = (unsigned short )0;
 sqlstm.sqtdso[0] = (unsigned short )0;
 sqlstm.sqphsv = sqlstm.sqhstv;
 sqlstm.sqphsl = sqlstm.sqhstl;
 sqlstm.sqphss = sqlstm.sqhsts;
 sqlstm.sqpind = sqlstm.sqindv;
 sqlstm.sqpins = sqlstm.sqinds;
 sqlstm.sqparm = sqlstm.sqharm;
 sqlstm.sqparc = sqlstm.sqharc;
 sqlstm.sqpadto = sqlstm.sqadto;
 sqlstm.sqptdso = sqlstm.sqtdso;
 sqlstm.sqlcmax = (unsigned int )100;
 sqlstm.sqlcmin = (unsigned int )2;
 sqlstm.sqlcincr = (unsigned int )1;
 sqlstm.sqlctimeout = (unsigned int )0;
 sqlstm.sqlcnowait = (unsigned int )0;
 sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
 if (sqlca.sqlcode < 0) sql_error();
}


	debug_out_stream  << "\nConnected to ORACLE.\n";

	debug_out_stream << "Call prepare_a_job_search_query"
						<< endl;
	by_country_region_state_city = prepare_a_job_search_query(dynamic_stmt,
					my_job_instance);
	my_job_instance.set_more_ematch_environ(debug_out_stream,
				by_country_region_state_city);

	debug_out_stream << "Return from set_more_ematch_environ\n";

	/* Allocate memory for the select and bind descriptors. */
	if (alloc_descriptors(MAX_SELECT_ITEMS,
                          MAX_VAR_NAME_LEN, MAX_IND_NAME_LEN) != 0)
		exit(1);

	debug_out_stream << "Return from alloc_descriptors\n";

	/* EXEC SQL PREPARE a_search_query  FROM  :dynamic_stmt; */ 

{
 struct sqlexd sqlstm;
 sqlorat((void **)0, &sqlctx, &oraca);
 sqlstm.sqlvsn = 13;
 sqlstm.arrsiz = 4;
 sqlstm.sqladtp = &sqladt;
 sqlstm.sqltdsp = &sqltds;
 sqlstm.stmt = "";
 sqlstm.iters = (unsigned int  )1;
 sqlstm.offset = (unsigned int  )36;
 sqlstm.cud = sqlcud0;
 sqlstm.sqlest = (unsigned char  *)&sqlca;
 sqlstm.sqlety = (unsigned short)4352;
 sqlstm.occurs = (unsigned int  )0;
 sqlstm.sqhstv[0] = (unsigned char  *)dynamic_stmt;
 sqlstm.sqhstl[0] = (unsigned long )4000;
 sqlstm.sqhsts[0] = (         int  )0;
 sqlstm.sqindv[0] = (         short *)0;
 sqlstm.sqinds[0] = (         int  )0;
 sqlstm.sqharm[0] = (unsigned long )0;
 sqlstm.sqadto[0] = (unsigned short )0;
 sqlstm.sqtdso[0] = (unsigned short )0;
 sqlstm.sqphsv = sqlstm.sqhstv;
 sqlstm.sqphsl = sqlstm.sqhstl;
 sqlstm.sqphss = sqlstm.sqhsts;
 sqlstm.sqpind = sqlstm.sqindv;
 sqlstm.sqpins = sqlstm.sqinds;
 sqlstm.sqparm = sqlstm.sqharm;
 sqlstm.sqparc = sqlstm.sqharc;
 sqlstm.sqpadto = sqlstm.sqadto;
 sqlstm.sqptdso = sqlstm.sqtdso;
 sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
 if (sqlca.sqlcode < 0) sql_error();
}

 
	/* EXEC SQL DECLARE dyn_4_cursor CURSOR FOR a_search_query; */ 
 

	set_bind_variables(debug_out_stream);

	debug_out_stream << "Return from set_bind_variables\n";

	/* EXEC SQL OPEN dyn_4_cursor
			USING DESCRIPTOR bind_dp; */ 

{
 struct sqlexd sqlstm;
 sqlorat((void **)0, &sqlctx, &oraca);
 sqlstm.sqlvsn = 13;
 sqlstm.arrsiz = 4;
 sqlstm.sqladtp = &sqladt;
 sqlstm.sqltdsp = &sqltds;
 sqlstm.stmt = "";
 sqlstm.iters = (unsigned int  )1;
 sqlstm.offset = (unsigned int  )55;
 sqlstm.selerr = (unsigned short)1;
 sqlstm.sqlpfmem = (unsigned int  )0;
 sqlstm.cud = sqlcud0;
 sqlstm.sqlest = (unsigned char  *)&sqlca;
 sqlstm.sqlety = (unsigned short)4352;
 sqlstm.occurs = (unsigned int  )0;
 sqlstm.sqcmod = (unsigned int )0;
 sqlstm.sqhstv[0] = (unsigned char  *)bind_dp;
 sqlstm.sqhstl[0] = (unsigned long )0;
 sqlstm.sqhsts[0] = (         int  )0;
 sqlstm.sqindv[0] = (         short *)0;
 sqlstm.sqinds[0] = (         int  )0;
 sqlstm.sqharm[0] = (unsigned long )0;
 sqlstm.sqadto[0] = (unsigned short )0;
 sqlstm.sqtdso[0] = (unsigned short )0;
 sqlstm.sqphsv = sqlstm.sqhstv;
 sqlstm.sqphsl = sqlstm.sqhstl;
 sqlstm.sqphss = sqlstm.sqhsts;
 sqlstm.sqpind = sqlstm.sqindv;
 sqlstm.sqpins = sqlstm.sqinds;
 sqlstm.sqparm = sqlstm.sqharm;
 sqlstm.sqparc = sqlstm.sqharc;
 sqlstm.sqpadto = sqlstm.sqadto;
 sqlstm.sqptdso = sqlstm.sqtdso;
 sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
 if (sqlca.sqlcode < 0) sql_error();
}

 

	/* EXEC SQL WHENEVER NOT FOUND DO break; */ 


	my_job_instance.initialize_result_array();

	num_of_matched_rows = retrieve_matched_job_rows(my_job_instance);

	my_job_instance.set_num_of_rows(num_of_matched_rows);

	debug_out_stream  << "Returned from ematch search" << endl;
	debug_out_stream << "Total " << num_of_matched_rows << " rows  returned" << endl;

	my_job_instance.print_neighbor_cities(debug_out_stream);
	my_job_instance.print_neighbor_states(debug_out_stream);
	my_job_instance.print_cities_in_states(debug_out_stream);
	my_job_instance.print_states_in_regions(debug_out_stream);


	my_job_instance.sort_result_rows(debug_out_stream);

	my_job_instance.print_result_rows(result_out_stream);
	//my_job_instance.print_result_rows(cout);

   	/* When done, free the memory allocated for
	   pointers in the bind and select descriptors. */
	for (i = 0; i < MAX_SELECT_ITEMS; i++)
	{    
		if (bind_dp->V[i] != (char *) 0)
			free(bind_dp->V[i]);
		free(bind_dp->I[i]);   /* MAX_ITEMS were allocated. */
		if (select_dp->V[i] != (char *) 0)
			free(select_dp->V[i]);
		free(select_dp->I[i]); /* MAX_ITEMS were allocated. */
	}

	/* Free space used by the descriptors themselves. */
	/*sqlclu(bind_dp);
	sqlclu(select_dp);
	*/
	/* EXEC SQL WHENEVER SQLERROR CONTINUE; */ 

	/* Close the cursor. */
	/* EXEC SQL CLOSE dyn_4_cursor; */ 

{
 struct sqlexd sqlstm;
 sqlorat((void **)0, &sqlctx, &oraca);
 sqlstm.sqlvsn = 13;
 sqlstm.arrsiz = 4;
 sqlstm.sqladtp = &sqladt;
 sqlstm.sqltdsp = &sqltds;
 sqlstm.iters = (unsigned int  )1;
 sqlstm.offset = (unsigned int  )74;
 sqlstm.cud = sqlcud0;
 sqlstm.sqlest = (unsigned char  *)&sqlca;
 sqlstm.sqlety = (unsigned short)4352;
 sqlstm.occurs = (unsigned int  )0;
 sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
}




	/* EXEC SQL COMMIT WORK RELEASE; */ 

{
 struct sqlexd sqlstm;
 sqlorat((void **)0, &sqlctx, &oraca);
 sqlstm.sqlvsn = 13;
 sqlstm.arrsiz = 4;
 sqlstm.sqladtp = &sqladt;
 sqlstm.sqltdsp = &sqltds;
 sqlstm.iters = (unsigned int  )1;
 sqlstm.offset = (unsigned int  )89;
 sqlstm.cud = sqlcud0;
 sqlstm.sqlest = (unsigned char  *)&sqlca;
 sqlstm.sqlety = (unsigned short)4352;
 sqlstm.occurs = (unsigned int  )0;
 sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
}


	debug_out_stream << "\nHave a good day!\n";

	/* EXEC SQL WHENEVER SQLERROR DO sql_error(); */ 


/*	debug_out_stream  << " Total " << i << " rows satisfying the specified conditions returned" << endl;
	exec sql close c1;
*/
	debug_out_stream.close();

	j=time(NULL);
	sprintf (copy_output_file, "%s %d.txt", "cp ematch_job_out.txt ", j);
	system (copy_output_file);
	//cout << j << ".txt " << num_of_matched_rows;

	exit(0);
}


/*
 * Prepare a SQL query from the given name=value pairs of CGI input string
 */
int prepare_a_job_search_query (char stmt[], ematch_class my_j_instance)

{

	int pair_number;
	int i, len;
	int is_country_region_state_or_city = 0;
	int search_by_country_region_state_or_city = 0;
	int is_string;

	int add_an_and_sign;
	int salary, country_code;

	int condition_number = 0;
	char buf[10];

	pair_number = my_j_instance.pair_number;

	debug_out_stream  << "Prepare a job_search_query from " << pair_number << " pair(s) of values\n";

	if (pair_number == 0) {
		strcpy (stmt, "select * from job");
		debug_out_stream << "The prepared SQL statement is: \n";
		debug_out_stream << " " << stmt << "\n";
		return 0;
	}
	else
		strcpy (stmt, "select * from job where "); // base query

	search_by_country_region_state_or_city = 0;

	//  Extract search information
	for (i = 0; i < pair_number; i++) {


		is_country_region_state_or_city = 0;

		is_string = 0;
		
		add_an_and_sign = 1;

		len = strlen (my_j_instance.value[i]);
	
		debug_out_stream  << my_j_instance.name[i] << "=" <<
				my_j_instance.value[i]  << " len=" << len << "&";

		if (len != 0) {
		if (strncmp(my_j_instance.name[i], "job_type", 8) == 0) {

			strcat (stmt, "job_type = '");

			is_string = 1;
			condition_number++;

		}
		else if (strcmp(my_j_instance.name[i], "job_title") == 0) {
			strcat (stmt, "job_title = '");

			is_string = 2;
			condition_number++;

		} else if (strcmp(my_j_instance.name[i], "specialization") == 0) {
			strcat (stmt, "specialization = '");

			is_string = 3;
			condition_number++;
		}
		else if (strcmp(my_j_instance.name[i], "country_code") == 0) {
			country_code = atoi(my_j_instance.value[i]);
			strcat (stmt, "country_code = ");
			sprintf (buf, "%d\0", country_code);
			strcat (stmt, buf);

			is_country_region_state_or_city = 1;
			search_by_country_region_state_or_city = 1;
			condition_number++;

		}
		// region, state, and location information is not placed in the query predicate
		// due to the need to rate rows. All rows will be first selected and then
		// rated according to the geographical location in the row and the required
		// geographical location.
		else if (strcmp(my_j_instance.name[i], "region_name") == 0) {
			//strcat (stmt, "region_name = '");

			is_country_region_state_or_city = 2;
			search_by_country_region_state_or_city = 2;
			add_an_and_sign = 0;
		}
		else if (strcmp(my_j_instance.name[i], "state_name") == 0) {
			//strcat (stmt, "state_name = '");

			is_country_region_state_or_city = 3;
			search_by_country_region_state_or_city = 3;
			add_an_and_sign = 0;
		}
		else if (strcmp(my_j_instance.name[i], "location") == 0) {
			// strcat (stmt, "location = '");

			is_country_region_state_or_city = 4;
			search_by_country_region_state_or_city = 4;
			debug_out_stream << "BY LOCATION!" << endl;
			add_an_and_sign = 0;
		}
		else if (strcmp(my_j_instance.name[i], "company_name") == 0) {
			strcat (stmt, "company_name = '");

			condition_number++;
			is_string = 4;
			condition_number++;
		}
		else if (strcmp(my_j_instance.name[i], "min_salary") == 0) {
			debug_out_stream << "In main debug salary\n";
			if (my_j_instance.salary_required == 0) {
				add_an_and_sign = 0;
				debug_out_stream << "add_an_and_sign=" 
						<< add_an_and_sign <<"\n";
			}
			else {
				salary = atoi(my_j_instance.value[i]);
				strcat (stmt, "min_salary >= 0");
				condition_number++;
			}
		}

		if (is_string) {
			strcat (stmt, my_j_instance.unchanged_value[i]);
			strcat (stmt, "'");
		}

		if ((i < pair_number - 1) && (add_an_and_sign == 1)) {
			debug_out_stream << "Put an and\n";
			strcat (stmt, " and ");
		}
		}

	}


	if (condition_number == 0)
		stmt[strlen(stmt)-7] = '\0';
	else {
		len = strlen(stmt);
			if ((stmt[len-1] == ' ') && (stmt[len-2] == 'd') &&
				(stmt[len-3] == 'n') && (stmt[len-4] == 'a') )
					// Get rid the last redundant "and"
					stmt[len-5] = '\0';
	}

	debug_out_stream << "The constructed JOB query statement is:\n";
	debug_out_stream << stmt << "----" << endl;
	debug_out_stream << "condition_number = " << condition_number << endl;

	debug_out_stream <<
		 "search_by_country_region_state_or_city="
			<< search_by_country_region_state_or_city << endl;

	return search_by_country_region_state_or_city ;


}   /* End of prepare_a_job_search_query */


int retrieve_matched_job_rows(ematch_class s_result)
{
	int i;

	int num_of_matched_rows = 0;
	int total_num_of_rows_processed = 0;

	int temp_rating;

	char temp_str[2000];
	my_string_class my_string_instance;

	mystring * one_temp_row_record;
	int *one_temp_row_record_ind;

	one_temp_row_record = new mystring [COLUMN_NUMBER_IN_JOB_TABLE];
	one_temp_row_record_ind = new int [COLUMN_NUMBER_IN_JOB_TABLE];

	for (i = 0; i < COLUMN_NUMBER_IN_JOB_TABLE; i++)
		one_temp_row_record[i] = new char [job_table_column_length[i]];

	if (pre_retrieval(debug_out_stream) < 0)
		exit (-1);
	
	debug_out_stream << endl;

	/* FETCH each row selected and print the column values. */
	/* EXEC SQL WHENEVER NOT FOUND GOTO end_select_loop; */ 


	for (;;)
	{
	    /* EXEC SQL FETCH dyn_4_cursor USING DESCRIPTOR select_dp; */ 

{
     struct sqlexd sqlstm;
     sqlorat((void **)0, &sqlctx, &oraca);
     sqlstm.sqlvsn = 13;
     sqlstm.arrsiz = 4;
     sqlstm.sqladtp = &sqladt;
     sqlstm.sqltdsp = &sqltds;
     sqlstm.iters = (unsigned int  )1;
     sqlstm.offset = (unsigned int  )104;
     sqlstm.selerr = (unsigned short)1;
     sqlstm.sqlpfmem = (unsigned int  )0;
     sqlstm.cud = sqlcud0;
     sqlstm.sqlest = (unsigned char  *)&sqlca;
     sqlstm.sqlety = (unsigned short)4352;
     sqlstm.occurs = (unsigned int  )0;
     sqlstm.sqfoff = (         int )0;
     sqlstm.sqfmod = (unsigned int )2;
     sqlstm.sqhstv[0] = (unsigned char  *)select_dp;
     sqlstm.sqhstl[0] = (unsigned long )0;
     sqlstm.sqhsts[0] = (         int  )0;
     sqlstm.sqindv[0] = (         short *)0;
     sqlstm.sqinds[0] = (         int  )0;
     sqlstm.sqharm[0] = (unsigned long )0;
     sqlstm.sqadto[0] = (unsigned short )0;
     sqlstm.sqtdso[0] = (unsigned short )0;
     sqlstm.sqphsv = sqlstm.sqhstv;
     sqlstm.sqphsl = sqlstm.sqhstl;
     sqlstm.sqphss = sqlstm.sqhsts;
     sqlstm.sqpind = sqlstm.sqindv;
     sqlstm.sqpins = sqlstm.sqinds;
     sqlstm.sqparm = sqlstm.sqharm;
     sqlstm.sqparc = sqlstm.sqharc;
     sqlstm.sqpadto = sqlstm.sqadto;
     sqlstm.sqptdso = sqlstm.sqtdso;
     sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
     if (sqlca.sqlcode == 1403) goto end_select_loop;
     if (sqlca.sqlcode < 0) sql_error();
}



		    total_num_of_rows_processed++;

		    debug_out_stream << "\nThe " << total_num_of_rows_processed << "th row: \n";

	    /* Since each variable returned has been coerced to a
	       character string, int, or float very little processing 
	       is required here.  This routine just prints out the 
	       values on the terminal. */
	    for (i = 0; i < select_dp->F; i++)
	    {
			    debug_out_stream << " The " << i+1 << "th column: ";


		if (*select_dp->I[i] < 0) {
		  /*  if (select_dp->T[i] == 4) 
		      debug_out_stream << (int)select_dp->L[i]+3;
		    else
		      debug_out_stream << (int)select_dp->L[i];
		      */
		    strcpy(temp_str,"\0");
		} else if (select_dp->T[i] == 3) {    /* int datatype */
					    debug_out_stream << "An integer " << *(int *) select_dp->V[i] << endl;
					    sprintf (temp_str, "%d", *(int *) select_dp->V[i]);
		} else if (select_dp->T[i] == 4) {    /* float datatype */
		    //  debug_out_stream <<  (int)select_dp->L[i] << 
		    //                 *(float *)select_dp->V[i];
					    sprintf(temp_str, "%f", *(float *)select_dp->V[i]);
		}
		else {                       /* character string */

				    my_string_instance.get_rid_of_padding_blanks(temp_str,select_dp->V[i],
																    select_dp->L[i]);
				    //printf ("%-*.*s ", (int)select_dp->L[i],
				    //		(int)select_dp->L[i], select_dp->V[i]);
				    // debug_out_stream << "L[i]=" << (int)select_dp->L[i] << "LL ";
				    // debug_out_stream << "VV-" << temp_str << "-vv\n";
		}

		debug_out_stream << "temp_str=" << temp_str << ",and len=" << strlen(temp_str)
					<< endl;
		//my_string_instance.to_lower(temp_str);
		//s_result.insert_a_col_to_result_array(temp_str, i, num_of_matched_rows,
		//		*select_dp->I[i]);

		strcpy(one_temp_row_record[i], temp_str);
		one_temp_row_record[i][strlen(temp_str)] = '\0';

		one_temp_row_record_ind[i] = *select_dp->I[i];
	    }

	    temp_rating = s_result.compute_a_job_rating
		    (one_temp_row_record, one_temp_row_record_ind, debug_out_stream);

	    if (temp_rating > 0) {
			    s_result.insert_a_matched_row(debug_out_stream,
					    one_temp_row_record, 
					    one_temp_row_record_ind, temp_rating);
			    num_of_matched_rows ++;
			    if (num_of_matched_rows >= MAX_MATCH_NUMBER) {
				    debug_out_stream << "TOTAL " << total_num_of_rows_processed
						    << " processed, and " << num_of_matched_rows <<
							    " matched" << endl;
				    return num_of_matched_rows;
			    }
	    }
	    //printf ("\n\n");
	}

end_select_loop:
	debug_out_stream << "TOTAL " << total_num_of_rows_processed
					 << " processed, and " << num_of_matched_rows <<
					   " matched" << endl;
    return num_of_matched_rows;
} /* end of retrieve_relevant_rows */


/*
 *  Prepare an SQL member search query, which will be returned through
 *		the parameter stmt.
 *
 */
int prepare_a_member_search_query(char *stmt, 
				ematch_class my_ematch_instance)
{
	int pair_number;
	int i, len;
	int search_by_country_region_state_or_city = 0;
	int is_string;

	int add_an_and_sign;  // Whether an 'and' connective should be added 
	int col_index;

	int degree, year_of_exp, salary;
	int current_job_location_code, location_code;

	int condition_number = 0;

	char buf[100];


	pair_number = my_ematch_instance.pair_number;

	debug_out_stream  << "Prepare a member search query from "
					<< pair_number << " pair(s) of values\n";

	if (pair_number == 0) {
		strcpy (stmt, "select * from member");
		return 0;
	}
	else
		strcpy (stmt, "select * from member where ");

	pair_number = my_ematch_instance.pair_number;

	//  Extract search information
	for (i = 0; i < pair_number; i++) {

		col_index = 0;
		
		is_string = 0;
		add_an_and_sign = 1;

		len = strlen (my_ematch_instance.value[i]);
	
		debug_out_stream  << my_ematch_instance.name[i] << "=" <<
				my_ematch_instance.value[i]  << " len=" << len << endl;

		if (strcmp(my_ematch_instance.name[i], "job_type") == 0) {

			strcat (stmt, "job_type = '");

			debug_out_stream << "my_ematch_instance.unchanged_value[i] = " <<
				my_ematch_instance.unchanged_value[i] << endl;
			add_an_and_sign = 1;
			is_string = 1;
			condition_number++;
		} else if (strcmp(my_ematch_instance.name[i], "job_title") == 0) {

			strcat (stmt, "job_title = '");

			debug_out_stream << "my_ematch_instance.unchanged_value[i] = " <<
				my_ematch_instance.unchanged_value[i] << endl;
			add_an_and_sign = 1;
			is_string = 1;
			condition_number++;
		} else if (strcmp(my_ematch_instance.name[i], "specialization") == 0) {

			strcat (stmt, "specialization = '");

			sprintf(buf, "%s", my_ematch_instance.unchanged_value[i]);

			add_an_and_sign = 1;
			is_string = 1;
			condition_number++;
		} else if (strcmp(my_ematch_instance.name[i], "current_job_location") == 0) {

			//strcat (stmt, "current_job_location = '");

			sprintf(buf, "%s", my_ematch_instance.unchanged_value[i]);
			debug_out_stream << "current_job_location = " <<
				buf << endl;
			add_an_and_sign = 0;
			// is_string = 1;
			// condition_number++;
		} else if (strcmp(my_ematch_instance.name[i], 
				"current_job_location_code") == 0){

			current_job_location_code = atoi(my_ematch_instance.value[i]);
			search_by_country_region_state_or_city =
					 current_job_location_code;
			debug_out_stream << "current_job_location_code = "
				<< current_job_location_code << endl;
			add_an_and_sign = 0;
		}

		else if (strncmp(my_ematch_instance.name[i], "year_of_exp", 11) == 0) {

			strcat (stmt, "year_of_exp >= ");
			year_of_exp = atoi(my_ematch_instance.value[i]);
			sprintf(buf, "%d\0", 0);
			strcat (stmt, buf);
			condition_number++;

		} else if (strcmp(my_ematch_instance.name[i], "degree") == 0) {

			strcat (stmt, "degree >= ");
			degree = atoi(my_ematch_instance.unchanged_value[i]);
			sprintf(buf, "%d\0", degree);
			strcat (stmt, buf);
			condition_number++;

		} else if (strcmp(my_ematch_instance.name[i], "desired_salary") == 0) {

			debug_out_stream << "In main debug member salary\n";
			if (my_ematch_instance.salary_required == 0) {
				add_an_and_sign = 0;
				debug_out_stream << "add_an_and_sign=" 
						<< add_an_and_sign <<"\n";
			}
			else {
				salary = atoi(my_ematch_instance.value[i]);
				strcat (stmt, "desired_salary >= 0");
				condition_number++;
			}
		} else if (strcmp(my_ematch_instance.name[i], "desired_job_location") == 0) {

			add_an_and_sign = 0;
		} else if (strcmp(my_ematch_instance.name[i], 
				"desired_job_location_code") == 0){

			location_code = atoi(my_ematch_instance.value[i]);
			search_by_country_region_state_or_city = location_code;
			debug_out_stream << "location_code = " << location_code << endl;
			add_an_and_sign = 0;
		}


		if (is_string) {
			strcat (stmt, my_ematch_instance.unchanged_value[i]);
			strcat (stmt, "'");
		}

		// Not the last condition, add an 'and' logical connective
		if ((i < pair_number - 1) && (add_an_and_sign == 1)) {
			debug_out_stream << "Put an and\n";
			strcat (stmt, " and ");

		}

	}


	if (condition_number == 0)
		stmt[strlen(stmt)-7] = '\0';
	else {
		len = strlen(stmt);
			if ((stmt[len-1] == ' ') && (stmt[len-2] == 'd') &&
				(stmt[len-3] == 'n') && (stmt[len-4] == 'a') )
					// Get rid the last redundant "and"
					stmt[len-5] = '\0';
	}

	debug_out_stream <<
		"The constructed MEMBER query statement is:\n";
	debug_out_stream << stmt << "----" << endl;
	debug_out_stream << "condition_number = " <<
		condition_number << endl;

	debug_out_stream <<
		 "search_by_country_region_state_or_city="
			<< search_by_country_region_state_or_city << endl;

	return search_by_country_region_state_or_city ;
}



void sql_error()
{
/* This is the Oracle error handler.
 * Print diagnostic text containing the error message,
 * current SQL statement, and location of error.
 */
    printf("\n%.*s\n",
       sqlca.sqlerrm.sqlerrml, sqlca.sqlerrm.sqlerrmc);
    printf("in \"%.*s...\"\n",
        oraca.orastxt.orastxtl, oraca.orastxt.orastxtc);
    printf("on line %d of %.*s.\n\n",
        oraca.oraslnr, oraca.orasfnm.orasfnml,
        oraca.orasfnm.orasfnmc);

/* Disable Oracle error checking to avoid an infinite loop
 * should another error occur within this routine as a 
 * result of the rollback.
 */
    /* EXEC SQL WHENEVER SQLERROR CONTINUE; */ 


/* Roll back any pending changes and disconnect from Oracle. */
    /* EXEC SQL ROLLBACK RELEASE; */ 

{
    struct sqlexd sqlstm;
    sqlorat((void **)0, &sqlctx, &oraca);
    sqlstm.sqlvsn = 13;
    sqlstm.arrsiz = 4;
    sqlstm.sqladtp = &sqladt;
    sqlstm.sqltdsp = &sqltds;
    sqlstm.iters = (unsigned int  )1;
    sqlstm.offset = (unsigned int  )123;
    sqlstm.cud = sqlcud0;
    sqlstm.sqlest = (unsigned char  *)&sqlca;
    sqlstm.sqlety = (unsigned short)4352;
    sqlstm.occurs = (unsigned int  )0;
    sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
}



    //exit(1);
}



/*
 *  Allocate the BIND and SELECT descriptors using sqlald().
 *  Also allocate the pointers to indicator variables
 *  in each descriptor.  The pointers to the actual bind
 *  variables and the select-list items are realloc'ed in
 *  the set_bind_variables() or process_select_list()
 *  routines.  This routine allocates 1 byte for select_dp->V[i]
 *  and bind_dp->V[i], so the realloc will work correctly.
 */

int alloc_descriptors(int size, int max_var_name_len, int max_ind_name_len)
{
    int i;

    /*
     * The first sqlald parameter determines the maximum number of
     * array elements in each variable in the descriptor. In
     * other words, it determines the maximum number of bind
     * variables or select-list items in the SQL statement.
     *
     * The second parameter determines the maximum length of
     * strings used to hold the names of select-list items
     * or placeholders.  The maximum length of column 
     * names in ORACLE is 30, but you can allocate more or less
     * as needed.
     *
     * The third parameter determines the maximum length of
     * strings used to hold the names of any indicator
     * variables.  To follow ORACLE standards, the maximum
     * length of these should be 30.  But, you can allocate
     * more or less as needed.
     */

    if ((bind_dp =
            sqlald(size, max_var_name_len, max_ind_name_len)) == (SQLDA *) 0)
    {
        fprintf(stderr,
            "Cannot allocate memory for bind descriptor.");
        return -1;  /* Have to exit in this case. */
    }

    if ((select_dp =
        sqlald (size, max_var_name_len, max_ind_name_len)) == (SQLDA *) 0)
    {
        fprintf(stderr,
            "Cannot allocate memory for select descriptor.");
        return -1;
    }
    select_dp->N = MAX_SELECT_ITEMS;

    /* Allocate the pointers to the indicator variables, and the
       actual data. */
    for (i = 0; i < MAX_SELECT_ITEMS; i++) {
        bind_dp->I[i] =  new short;
        select_dp->I[i] =  new short;
        bind_dp->V[i] = new char[1];
        select_dp->V[i] = new char[1];
    }
       
    return 0;
}
 


int set_bind_variables(ofstream &debug_out_stream)
{
    int i, n;
    char bind_var[64];

    /* Describe any bind variables (input host variables) */
    /* EXEC SQL WHENEVER SQLERROR DO sql_error(); */ 


    bind_dp->N = MAX_SELECT_ITEMS;  /* Init. count of array elements. */

    /* EXEC SQL DESCRIBE BIND VARIABLES FOR a_search_query INTO bind_dp; */ 

{
    struct sqlexd sqlstm;
    sqlorat((void **)0, &sqlctx, &oraca);
    sqlstm.sqlvsn = 13;
    sqlstm.arrsiz = 4;
    sqlstm.sqladtp = &sqladt;
    sqlstm.sqltdsp = &sqltds;
    sqlstm.iters = (unsigned int  )1;
    sqlstm.offset = (unsigned int  )138;
    sqlstm.cud = sqlcud0;
    sqlstm.sqlest = (unsigned char  *)&sqlca;
    sqlstm.sqlety = (unsigned short)4352;
    sqlstm.occurs = (unsigned int  )0;
    sqlstm.sqhstv[0] = (unsigned char  *)bind_dp;
    sqlstm.sqhstl[0] = (unsigned long )0;
    sqlstm.sqhsts[0] = (         int  )0;
    sqlstm.sqindv[0] = (         short *)0;
    sqlstm.sqinds[0] = (         int  )0;
    sqlstm.sqharm[0] = (unsigned long )0;
    sqlstm.sqadto[0] = (unsigned short )0;
    sqlstm.sqtdso[0] = (unsigned short )0;
    sqlstm.sqphsv = sqlstm.sqhstv;
    sqlstm.sqphsl = sqlstm.sqhstl;
    sqlstm.sqphss = sqlstm.sqhsts;
    sqlstm.sqpind = sqlstm.sqindv;
    sqlstm.sqpins = sqlstm.sqinds;
    sqlstm.sqparm = sqlstm.sqharm;
    sqlstm.sqparc = sqlstm.sqharc;
    sqlstm.sqpadto = sqlstm.sqadto;
    sqlstm.sqptdso = sqlstm.sqtdso;
    sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
    if (sqlca.sqlcode < 0) sql_error();
}



    /* If F is negative, there were more bind variables
       than originally allocated by SQLSQLDAAlloc(). */
    if (bind_dp->F < 0) {

        debug_out_stream  << "\nToo many bind variables " << -(bind_dp->F)  << ", maximum is ";
		debug_out_stream  << MAX_SELECT_ITEMS << endl;
        return -1;
    }

    /* Set the maximum number of array elements in the
       descriptor to the number found. */

    bind_dp->N = bind_dp->F;
 
    /* Get the value of each bind variable as a
     * character string.
     *   
     * C[i] contains the length of the bind variable
     *      name used in the SQL statement.
     * S[i] contains the actual name of the bind variable
     *      used in the SQL statement.
     *
     * L[i] will contain the length of the data value
     *      entered.
     *
     * V[i] will contain the address of the data value
     *      entered.
     *
     * T[i] is always set to 1 because in this sample program
     *      data values for all bind variables are entered
     *      as character strings.
     *      ORACLE converts to the table value from CHAR.
     *
     * I[i] will point to the indicator value, which is
     *      set to -1 when the bind variable value is "null".
     */


    for (i = 0; i < bind_dp->F; i++)
    {
        debug_out_stream << "\nEnter value for bind variable ";
		debug_out_stream << setw((int)bind_dp->C[i]) << bind_dp->S[i] << "s:  ";

        fgets(bind_var, sizeof bind_var, stdin);

        /* Get length and remove the new line character. */
        n = strlen(bind_var) - 1;

        /* Set it in the descriptor. */
        bind_dp->L[i] = n;

        /* (re-)allocate the buffer for the value.
           SQLSQLDAAlloc() reserves a pointer location for
           V[i] but does not allocate the full space for
           the pointer. */

         bind_dp->V[i] = (char *) realloc(bind_dp->V[i],
                         (bind_dp->L[i] + 1));            

        /* And copy it in. */
        strncpy(bind_dp->V[i], bind_var, n);

        /* Set the indicator variable's value. */
        if ((strncmp(bind_dp->V[i], "NULL", 4) == 0) ||
                (strncmp(bind_dp->V[i], "null", 4) == 0))
            *bind_dp->I[i] = -1;
        else
            *bind_dp->I[i] = 0;
    
        /* Set the bind datatype to 1 for CHAR. */
        bind_dp->T[i] = 1;
    }
	return 0;
}
 

int pre_retrieval(ofstream &out_stream)
{
	int i, null_ok, precision, scale;

    /* If the SQL statement is a SELECT, describe the
        select-list items.  The DESCRIBE function returns
        their names, datatypes, lengths (including precision
        and scale), and NULL/NOT NULL statuses. */

    select_dp->N = MAX_SELECT_ITEMS;
    
    /* EXEC SQL DESCRIBE SELECT LIST FOR a_search_query INTO select_dp; */ 

{
    struct sqlexd sqlstm;
    sqlorat((void **)0, &sqlctx, &oraca);
    sqlstm.sqlvsn = 13;
    sqlstm.arrsiz = 4;
    sqlstm.sqladtp = &sqladt;
    sqlstm.sqltdsp = &sqltds;
    sqlstm.iters = (unsigned int  )1;
    sqlstm.offset = (unsigned int  )157;
    sqlstm.cud = sqlcud0;
    sqlstm.sqlest = (unsigned char  *)&sqlca;
    sqlstm.sqlety = (unsigned short)4352;
    sqlstm.occurs = (unsigned int  )0;
    sqlstm.sqhstv[0] = (unsigned char  *)select_dp;
    sqlstm.sqhstl[0] = (unsigned long )0;
    sqlstm.sqhsts[0] = (         int  )0;
    sqlstm.sqindv[0] = (         short *)0;
    sqlstm.sqinds[0] = (         int  )0;
    sqlstm.sqharm[0] = (unsigned long )0;
    sqlstm.sqadto[0] = (unsigned short )0;
    sqlstm.sqtdso[0] = (unsigned short )0;
    sqlstm.sqphsv = sqlstm.sqhstv;
    sqlstm.sqphsl = sqlstm.sqhstl;
    sqlstm.sqphss = sqlstm.sqhsts;
    sqlstm.sqpind = sqlstm.sqindv;
    sqlstm.sqpins = sqlstm.sqinds;
    sqlstm.sqparm = sqlstm.sqharm;
    sqlstm.sqparc = sqlstm.sqharc;
    sqlstm.sqpadto = sqlstm.sqadto;
    sqlstm.sqptdso = sqlstm.sqtdso;
    sqlcxt((void **)0, &sqlctx, &sqlstm, &sqlfpn);
    if (sqlca.sqlcode < 0) sql_error();
}



    /* If F is negative, there were more select-list
       items than originally allocated by sqlald(). */
	
    if (select_dp->F < 0)
    {
    out_stream  << "\nToo many select-list items (" <<  -(select_dp->F) << "), maximum is ";
	out_stream  <<  MAX_SELECT_ITEMS << endl;
        return -1;
    }

	
    /* Set the maximum number of array elements in the
       descriptor to the number found. */
    select_dp->N = select_dp->F;

    /* Allocate storage for each select-list item.
  
       sqlprc() is used to extract precision and scale
       from the length (select_dp->L[i]).

       sqlnul() is used to reset the high-order bit of
       the datatype and to check whether the column
       is NOT NULL.

       CHAR    datatypes have length, but zero precision and
               scale.  The length is defined at CREATE time.

       NUMBER  datatypes have precision and scale only if
               defined at CREATE time.  If the column
               definition was just NUMBER, the precision
               and scale are zero, and you must allocate
               the required maximum length.

       DATE    datatypes return a length of 7 if the default
               format is used.  This should be increased to
               9 to store the actual date character string.
               If you use the TO_CHAR function, the maximum
               length could be 75, but will probably be less
               (you can see the effects of this in SQL*Plus).

       ROWID   datatype always returns a fixed length of 18 if
               coerced to CHAR.

       LONG and
       LONG RAW datatypes return a length of 0 (zero),
               so you need to set a maximum.  In this example,
               it is 240 characters.

       */
    
    out_stream << endl;
    for (i = 0; i < select_dp->F; i++)
    {
        /* Turn off high-order bit of datatype (in this example,
           it does not matter if the column is NOT NULL). */
        sqlnul ((unsigned short *) & 
		(select_dp->T[i]), (unsigned short *)&(select_dp->T[i]), &null_ok);


        switch (select_dp->T[i])
        {
            case  1 : /* CHAR datatype: no change in length
                         needed, except possibly for TO_CHAR
                         conversions (not handled here). */
                break;
            case  2 : /* NUMBER datatype: use sqlprc() to
                         extract precision and scale. */
                sqlprc ((unsigned int *)&(select_dp->L[i]), &precision, &scale);
                      /* Allow for maximum size of NUMBER. */
                if (precision == 0) precision = 40;
                      /* Also allow for decimal point and
                         possible sign. */
                /* convert NUMBER datatype to FLOAT if scale > 0,
                   INT otherwise. */
                if (scale > 0)
                    select_dp->L[i] = sizeof(float);
                else
                    select_dp->L[i] = sizeof(int);
                break;

            case  8 : /* LONG datatype */
                select_dp->L[i] = 240;
                break;

            case 11 : /* ROWID datatype */
                select_dp->L[i] = 18;
                break;

            case 12 : /* DATE datatype */
                select_dp->L[i] = 9;
                break;
 
            case 23 : /* RAW datatype */
                break;

            case 24 : /* LONG RAW datatype */
                select_dp->L[i] = 240;
                break;
        }
        /* Allocate space for the select-list data values.
           sqlald() reserves a pointer location for
           V[i] but does not allocate the full space for
           the pointer.  */

         if (select_dp->T[i] != 2)
           select_dp->V[i] = (char *) realloc(select_dp->V[i],
                                    select_dp->L[i] + 1);  
         else
           select_dp->V[i] = (char *) realloc(select_dp->V[i],
                                    select_dp->L[i]);  

        /* Print column headings, right-justifying number
            column headings. */
        if (select_dp->T[i] == 2)
           if (scale > 0) 
				out_stream << setw(select_dp->L[i]+3) << select_dp->S[i];
           else
				out_stream << setw(select_dp->L[i]) << select_dp->S[i];
        else {
			out_stream.setf(ios::left);
            out_stream << setw( select_dp->L[i]) << select_dp->S[i];
		}

        /* Coerce ALL datatypes except for LONG RAW and NUMBER to
           character. */
        if (select_dp->T[i] != 24 && select_dp->T[i] != 2)
            select_dp->T[i] = 1;

        /* Coerce the datatypes of NUMBERs to float or int depending on
           the scale. */
        if (select_dp->T[i] == 2)
          if (scale > 0)
             select_dp->T[i] = 4;  /* float */
          else
             select_dp->T[i] = 3;  /* int */
    }
    out_stream << "\n\n";

	return 0;
} /* end of pre_retrieval(ofstream) */


