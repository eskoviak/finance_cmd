-- issue_30_alters.sql
-- Applies changes from Issue #30 to both finance and finance_tst schemas

-- 1. Changes to finance schema
ALTER TABLE finance.external_accounts ALTER COLUMN account_type TYPE character varying(10);
ALTER TABLE finance.external_accounts ADD COLUMN active boolean DEFAULT true;
ALTER TABLE finance.accounts_payable ADD COLUMN vendor_account integer REFERENCES finance.external_accounts(external_account_id);

-- 2. Changes to finance_tst schema
ALTER TABLE finance_tst.external_accounts ALTER COLUMN account_type TYPE character varying(10);
ALTER TABLE finance_tst.external_accounts ADD COLUMN active boolean DEFAULT true;
ALTER TABLE finance_tst.accounts_payable ADD COLUMN vendor_account integer REFERENCES finance_tst.external_accounts(external_account_id);
