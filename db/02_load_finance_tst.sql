-- =============================================================================
-- 02_load_finance_tst.sql
-- Loads a working subset from finance into finance_tst (Issue #34)
--
-- Strategy:
--   Lookups         : full copy (all rows — these are small reference tables)
--   voucher         : last 100 rows by voucher_number DESC
--   voucher_detail  : all detail rows for those 100 vouchers
--   accounts_payable: rows whose payment_voucher_id is NULL or in loaded set
--   asset_transfer  : full copy (small table)
--
-- Run AFTER 01_recreate_finance_tst.sql
-- Run as: psql -d finance -f db/02_load_finance_tst.sql
-- =============================================================================

BEGIN;

\echo '== [1/7] Loading lookup: company =='
INSERT INTO finance_tst.company (id, company_number, company_name)
SELECT id, company_number, company_name
FROM finance.company;

\echo '== [2/7] Loading lookup: payment_type =='
INSERT INTO finance_tst.payment_type (payment_type_id, payment_type_text)
SELECT payment_type_id, payment_type_text
FROM finance.payment_type;

\echo '== [3/7] Loading lookup: voucher_type =='
INSERT INTO finance_tst.voucher_type (type_code, type_text)
SELECT type_code, type_text
FROM finance.voucher_type;

\echo '== [4/7] Loading lookup: vendors (full) =='
INSERT INTO finance_tst.vendors (vendor_number, vendor_short_desc, vendor_address)
SELECT vendor_number, vendor_short_desc, vendor_address
FROM finance.vendors;

\echo '== [5/7] Loading lookup: external_accounts (full) =='
INSERT INTO finance_tst.external_accounts (
    external_account_id, account_name, account_number, qualified, account_type)
SELECT external_account_id, account_name, account_number, qualified, account_type
FROM finance.external_accounts;

\echo '== [6/7] Loading transactions =='

-- voucher: last 100 by voucher_number (highest = most recent)
INSERT INTO finance_tst.voucher (
    voucher_number, voucher_date, voucher_ref, voucher_amt,
    voucher_type_id, vendor_number, payment_type_id,
    payment_ref, payment_source_id, company_id)
SELECT
    voucher_number, voucher_date, voucher_ref, voucher_amt,
    voucher_type_id, vendor_number, payment_type_id,
    payment_ref, payment_source_id, company_id
FROM finance.voucher
ORDER BY voucher_number DESC
LIMIT 100;

-- voucher_detail: all lines for the 100 vouchers loaded above
INSERT INTO finance_tst.voucher_detail (
    id, voucher_number, split_seq_number, account_number,
    amount, dimension_1, dimension_2, memo)
SELECT
    id, voucher_number, split_seq_number, account_number,
    amount, dimension_1, dimension_2, memo
FROM finance.voucher_detail
WHERE voucher_number IN (SELECT voucher_number FROM finance_tst.voucher);

-- accounts_payable: only rows whose payment_voucher_id references a loaded voucher
-- (or is NULL — unpaid statements have no voucher yet)
INSERT INTO finance_tst.accounts_payable (
    id, vendor_number, stmt_dt, stmt_amt, payment_due_dt,
    payment_source_id, payment_voucher_id, invoice_id)
SELECT
    id, vendor_number, stmt_dt, stmt_amt, payment_due_dt,
    payment_source_id, payment_voucher_id, invoice_id
FROM finance.accounts_payable
WHERE payment_voucher_id IS NULL
   OR payment_voucher_id IN (SELECT voucher_number FROM finance_tst.voucher);

-- asset_transfer: full copy (small table)
INSERT INTO finance_tst.asset_transfer (
    id, transfer_date, transfer_amount,
    src_external_account_id, tgt_external_account_id, memo)
SELECT
    id, transfer_date, transfer_amount,
    src_external_account_id, tgt_external_account_id, memo
FROM finance.asset_transfer;

\echo '== [7/7] Resetting sequences to max loaded values =='

SELECT setval('finance_tst.company_id_seq',
    COALESCE((SELECT MAX(id) FROM finance_tst.company), 1));
SELECT setval('finance_tst.payment_type_payment_type_id_seq',
    COALESCE((SELECT MAX(payment_type_id) FROM finance_tst.payment_type), 1));
SELECT setval('finance_tst.voucher_type_type_code_seq',
    COALESCE((SELECT MAX(type_code) FROM finance_tst.voucher_type), 1));
SELECT setval('finance_tst.vendors_vendor_number_seq',
    COALESCE((SELECT MAX(vendor_number) FROM finance_tst.vendors), 1));
SELECT setval('finance_tst.external_accounts_external_account_id_seq',
    COALESCE((SELECT MAX(external_account_id) FROM finance_tst.external_accounts), 1));
SELECT setval('finance_tst.voucher_voucher_number_seq',
    COALESCE((SELECT MAX(voucher_number) FROM finance_tst.voucher), 1));
SELECT setval('finance_tst.voucher_detail_id_seq',
    COALESCE((SELECT MAX(id) FROM finance_tst.voucher_detail), 1));
SELECT setval('finance_tst.accounts_payable_id_seq',
    COALESCE((SELECT MAX(id) FROM finance_tst.accounts_payable), 1));
SELECT setval('finance_tst.asset_transfer_id_seq',
    COALESCE((SELECT MAX(id) FROM finance_tst.asset_transfer), 1));

COMMIT;

\echo '== Load complete — row counts =='

SELECT table_name, row_count FROM (
    SELECT 'company'          AS table_name, COUNT(*) AS row_count FROM finance_tst.company          UNION ALL
    SELECT 'payment_type',                   COUNT(*)              FROM finance_tst.payment_type      UNION ALL
    SELECT 'voucher_type',                   COUNT(*)              FROM finance_tst.voucher_type      UNION ALL
    SELECT 'vendors',                        COUNT(*)              FROM finance_tst.vendors           UNION ALL
    SELECT 'external_accounts',              COUNT(*)              FROM finance_tst.external_accounts UNION ALL
    SELECT 'voucher',                        COUNT(*)              FROM finance_tst.voucher           UNION ALL
    SELECT 'voucher_detail',                 COUNT(*)              FROM finance_tst.voucher_detail    UNION ALL
    SELECT 'accounts_payable',               COUNT(*)              FROM finance_tst.accounts_payable  UNION ALL
    SELECT 'asset_transfer',                 COUNT(*)              FROM finance_tst.asset_transfer
) counts
ORDER BY table_name;
