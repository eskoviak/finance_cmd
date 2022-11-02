#include <stdlib.h>
#include "pg_finance_dao.h"

/*
 * internal functions
 */
static void
__exit_nicely__(PGconn *conn)
{
    PQfinish(conn);
    exit(1);
}

/* 
 * External functions */
 PGsearch_vendor(char* search_phrase)
{

}





int 
main(int argc, char** argv)
{
    const char  *conninfo;
    PGconn      *conn;
    PGresult    *res;
    int         nFields;
    int         i,j;

    /*
     * Parse the command line
     */
    if(argc > 1)
        conninfo = argv[1];
    else
        conninfo = "dbname = finance";

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
        res = PQexec(conn, 
                "SELECT pg_catalog.set_config('search_path', '', false)"
        );
        if (PQresultStatus(res) != PGRES_TUPLES_OK)
        {
            fprintf(stderr, "SET failed: %s", PQerrorMessage(conn));
            PQclear(res);
            exit_nicely(conn);
        }

        PQclear(res);

        /* Start a transaction block */
        res = PQexec(conn, "BEGIN");

        if (PQresultStatus(res) != PGRES_COMMAND_OK )
        {
            fprintf(stderr, "BEGIN failed: %s", PQerrorMessage(conn));
            PQclear(res);
            exit_nicely(conn);
        }
        PQclear(res);

        /* DECLARE the cursor */
        res = PQexec(conn,
                "DECLARE vendors CURSOR FOR \
                SELECT vendor_number, vendor_short_desc FROM finance.vendors WHERE vendor_short_desc ILIKE ('%wal%');"
        );
        if (PQresultStatus(res) != PGRES_COMMAND_OK )
        {
            fprintf(stderr, "DECLARE CURSOR failed: %s", PQerrorMessage(conn));
            PQclear(res);
            exit_nicely(conn);
        }
        PQclear(res);

        res = PQexec(conn,
                "FETCH ALL in vendors;"
        );
        if (PQresultStatus(res) != PGRES_TUPLES_OK )
        {
            fprintf(stderr, "FETCH ALL failed: %s", PQerrorMessage(conn));
            PQclear(res);
            exit_nicely(conn);
        }

        /* Print column headers*/
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

        res = PQexec(conn, "CLOSE vendors;");
        PQclear(res);

        res = PQexec(conn,
                "END;"
        );
        PQclear(res);

        PQfinish(conn);

        return 0;
    }

}   