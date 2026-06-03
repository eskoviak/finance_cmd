-- =============================================================================
-- 03_cleanup_external_accounts.sql
-- Applies external account cleanup adjustments in finance_tst.
--
-- Run AFTER 01_recreate_finance_tst.sql and 02_load_finance_tst.sql
-- Run as: psql -d finance -f db/03_cleanup_external_accounts.sql
-- =============================================================================

BEGIN;

\echo '== [1/5] Syncing external_accounts fields from finance =='
UPDATE finance_tst.external_accounts tst
SET
    account_name = src.account_name,
    account_type = src.account_type,
    active = src.active
FROM finance.external_accounts src
WHERE tst.external_account_id = src.external_account_id;

\echo '== [2/5] Ensuring external_account_id 10207 exists in finance_tst =='
INSERT INTO finance_tst.external_accounts (
    external_account_id, account_name, account_number, qualified, account_type, active
)
SELECT
    external_account_id, account_name, account_number, qualified, account_type, active
FROM finance.external_accounts
WHERE external_account_id = 10207
ON CONFLICT (external_account_id) DO UPDATE
SET
    account_name = EXCLUDED.account_name,
    account_number = EXCLUDED.account_number,
    qualified = EXCLUDED.qualified,
    account_type = EXCLUDED.account_type,
    active = EXCLUDED.active;

\echo '== [3/5] Updating debit vouchers from 19970 and 17542 to 10207 =='
UPDATE finance_tst.voucher
SET payment_source_id = 10207
WHERE payment_type_id = 10
  AND payment_source_id IN (19970, 17542);

\echo '== [4/5] Validating voucher source cleanup =='
DO $$
DECLARE
    remaining_19970 integer;
    remaining_17542 integer;
BEGIN
    SELECT COUNT(*)
      INTO remaining_19970
      FROM finance_tst.voucher
     WHERE payment_source_id = 19970
       AND payment_type_id = 10;

    SELECT COUNT(*)
      INTO remaining_17542
      FROM finance_tst.voucher
     WHERE payment_source_id = 17542
       AND payment_type_id = 10;

    IF remaining_19970 > 0 OR remaining_17542 > 0 THEN
        RAISE EXCEPTION
            'Cleanup validation failed. Remaining rows: 19970=% 17542=%',
            remaining_19970, remaining_17542;
    END IF;
END
$$;

\echo '== [5/5] Removing deprecated external_account_id 19970 =='
DELETE FROM finance_tst.external_accounts
WHERE external_account_id = 19970;

COMMIT;

\echo '== Cleanup complete =='
