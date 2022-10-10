#include <stdio.h>
#include <stdlib.h>
#include "libpq-fe.h"

/*
 * Make sure to clean up
 */
static void
exit_nicely(PGconn *conn)
{
    PQfinish(conn);
    exit(1);
}

int 
main(int argc, char** argv)
{
    const char  *conninfo;
    PGconn      *conn;
    PGresult    *res;
    int         nFields;
    int         i,j;
    const char  *schema;
    const char  *search_phrase;
    const char  *command;
    const Oid   *paramTypes;
    const char  *paramValues[1];
    int         paramLengths[1];
    int         paramFormats[1];

    /*
     * Parse the command line
     */
    if(argc > 1)
        conninfo = argv[1];
    else
        conninfo = "dbname = finance";

    schema = "finance_tst";
    search_phrase = "wal";
    
    /*
     * Connect to the database
     */
    conn = PQconnectdb(conninfo);

    /*
     * Check the status -- if connected, set always-secure search path
     */
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "%s", PQerrorMessage(conn));
        exit_nicely(conn);
    }
    else
    {
        /* set safe search path */
        //sprintf(command, "SET search_path = %s", schema);
        //res = PQexec(conn, "SET search_path = 'finance_tst'");
        //if (PQresultStatus(res) != PGRES_TUPLES_OK)
        //{
        //    fprintf(stderr, "SET failed: %s", PQerrorMessage(conn));
        //    PQclear(res);
        //    exit_nicely(conn);
        //}
        //PQclear(res);

        /* 
         * Test the parameterized search
         * $1 = search phrase
         */
        command = "SELECT vendor_number, vendor_short_desc FROM finance_tst.vendors WHERE \
            vendor_short_desc ILIKE '%$1%';";

        paramValues[0] = search_phrase;
        paramLengths[0] = sizeof(search_phrase);
        paramFormats[0] = 0;

        res = PQexecParams(conn,
                command,
                1,
                NULL,
                paramValues,
                paramLengths,
                paramFormats,
                0);
        if (PQresultStatus(res) != PGRES_TUPLES_OK )
        {
            fprintf(stderr, "SELECT failed: %s", PQerrorMessage(conn));
            PQclear(res);
            exit_nicely(conn);
        }        
        PQclear(res);   
        

        PQfinish(conn);

        return 0;
    }

}   