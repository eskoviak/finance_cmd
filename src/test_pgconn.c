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
    char        *conninfo;
    PGconn      *conn;
    PGresult    *res;
    int         nFields;
    int         i,j;
    const char  *schema = "finance_tst";
    const char  *search_phrase;
    char        *command;
    const Oid   *paramTypes;
    const char  *paramValues[1];
    int         paramLengths[1];
    int         paramFormats[1];
    int         debug = 1;

    /*
     * Parse the command line
     */
    if(argc > 1)
        conninfo = argv[1];
    else
        search_phrase = "spi";
        conninfo = "postgresql://postgres:terces##@localhost:5432/finance";

    
    /*
     * Connect to the database
     */
    conn = PQconnectdb(conninfo);

    /*
     * Check the status -- if connected, set always-secure search path
     */
    if (PQstatus(conn) != CONNECTION_OK)
    {
        fprintf(stderr, "%s\n", PQerrorMessage(conn));
        exit_nicely(conn);
    }
    else
    {
        /* set safe search path */
        sprintf(command, "SET search_path = '%s';", schema);
        fprintf(stderr, "SET search: %s\n", command);
        
        res = PQexec(conn, command);
        if (PQresultStatus(res) != PGRES_COMMAND_OK)
        {
            fprintf(stderr, "SET failed: %s", PQerrorMessage(conn));
            PQclear(res);
            exit_nicely(conn);
        }
        PQclear(res);
        

        /* 
         * Test the parameterized search
         * $1 = search phrase
         */
        command = "SELECT vendor_number, vendor_short_desc FROM vendors WHERE \
            UPPER(vendor_short_desc) ~ UPPER($1)";

        fprintf(stderr, "SELECT: %s\n", command);

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

        /* Select succeeded
         * Print column headers
         */
        nFields = PQnfields(res);
        for(i = 0; i < nFields; i++) printf("%-15s", PQfname(res, i));
        printf("\n\n");

        /* print the results */
        for (i = 0; i < PQntuples(res); i++)
        {
            for(j = 0; j < nFields; j++) printf("%-15s", PQgetvalue(res, i, j));
            printf("\n");
        }
        
        PQclear(res);
        PQfinish(conn);

        return 0;
    }

}   