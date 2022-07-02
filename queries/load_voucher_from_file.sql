--SQL to load voucher.csv
COPY finance.voucher(voucher_number,voucher_date,voucher_ref,voucher_amt,voucher_type_id,vendor_number,
    payment_type_id,payment_ref,payment_source_id)
FROM '/Users/edmundlskoviak/Documents/repos/finance_cmd/voucher.csv'
DELIMITER ','
CSV HEADER;