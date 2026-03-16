# Release and Design Notes for MyFinance Data Classes

## Some issues noted whilst doing reverse engineering the data model

1. While `finance.vendors` is set up to use the sequence structure for `vendor_number` as indicated; there are outliers that will break that construct.  Noteably from 3002 an above.  Currenly there is a query [get_next_vendor_number.sql](/Users/edmundlskoviak/Queries/get_next_vendor_number.sql) in the global Query director which gets the next number less than 2000.  This is a temporary fix.

