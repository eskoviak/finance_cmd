-- To allow longer account type names on  
alter table external_accounts alter column account_type type  varchar(45);

-- update account_type based on the first digit of external_account_id
-- to match the Chart of Accounts
UPDATE finance.external_accounts
SET account_type = 'Assets'
WHERE external_account_id BETWEEN 10000 AND 19999;

UPDATE finance.external_accounts
SET account_type = 'Liabilites'
WHERE external_account_id BETWEEN 20000 AND 29999;

UPDATE finance.external_accounts
SET account_type = 'Equity'
WHERE external_account_id BETWEEN 30000 AND 39999;

UPDATE finance.external_accounts
SET account_type = 'Revenue'
WHERE external_account_id BETWEEN 40000 AND 49999;

UPDATE finance.external_accounts
SET account_type = 'Expense'
WHERE external_account_id BETWEEN 50000 AND 59999;

UPDATE finance.external_accounts
SET account_type = 'Other (non-op) Revenue and Expense'
WHERE external_account_id BETWEEN 60000 AND 69999;

UPDATE finance.external_accounts
SET account_type = 'Intercompany And Related Party Accounts'
WHERE external_account_id BETWEEN 70000 AND 79999;

UPDATE finance.external_accounts
SET account_type = 'Acquisitions In Progress'
WHERE external_account_id BETWEEN 80000 AND 89999;

UPDATE finance.external_accounts
SET account_type = 'Misc Custom'
WHERE external_account_id BETWEEN 90000 AND 99999;

--Create the cross-reference table--Indicates the allowed payment sources for each type
DROP TABLE IF EXISTS finance.pmt_type_pmt_src_xref;

CREATE TABLE finance.pmt_type_pmt_src_xref (
    id SERIAL PRIMARY KEY,
    payment_type_id integer NOT NULL,
    external_account_id integer NOT NULL
);

--DELETE FROM finance.pmt_type_pmt_src_xref;
INSERT INTO finance.pmt_type_pmt_src_xref
(payment_type_id, external_account_id)
VALUES
(1, 17133),
(2, 17133),
(4, 19998),
(10,11005),
(10,13415)