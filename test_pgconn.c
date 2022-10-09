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
                "DECLARE vendors CURSOR FOR SELECT finance.search_vendor('wal');"
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

        nFields = PQnfields(res);
        /* print the results */
        for (i = 0; i < PQntuples(res); i++)
        {
            for(j = 0; j < nFields; j++)
            {
                printf("%-15s", PQgetvalue(res, i, j));
                printf("\n");
            }
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