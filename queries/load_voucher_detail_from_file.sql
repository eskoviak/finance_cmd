--SQL to load voucher.csv
COPY finance.voucher_detail(id,voucher_number,split_seq_number,account_number,amount,dimension_1,dimension_2,memo)
FROM '/Users/edmundlskoviak/Documents/repos/finance_cmd/voucher_detail.csv'
DELIMITER ','
CSV HEADER;