-- =============================================================================
-- 01_recreate_finance_tst.sql
-- Drops and recreates all tables in finance_tst matching the finance schema.
-- Scope: MVP subset for UI tech-testing (Issue #34)
--   Lookups : company, payment_type, voucher_type, vendors, external_accounts
--   Transactions: voucher, voucher_detail, accounts_payable, asset_transfer
-- Run as: psql -d finance -f db/01_recreate_finance_tst.sql
-- =============================================================================

\echo '== [1/4] Dropping existing tables =='

DROP TABLE IF EXISTS finance_tst.accounts_payable  CASCADE;
DROP TABLE IF EXISTS finance_tst.asset_transfer     CASCADE;
DROP TABLE IF EXISTS finance_tst.voucher_detail     CASCADE;
DROP TABLE IF EXISTS finance_tst.voucher            CASCADE;
DROP TABLE IF EXISTS finance_tst.external_accounts  CASCADE;
DROP TABLE IF EXISTS finance_tst.vendors            CASCADE;
DROP TABLE IF EXISTS finance_tst.payment_type       CASCADE;
DROP TABLE IF EXISTS finance_tst.voucher_type       CASCADE;
DROP TABLE IF EXISTS finance_tst.company            CASCADE;
-- leftover tables from previous partial setup
DROP TABLE IF EXISTS finance_tst.assets             CASCADE;
DROP TABLE IF EXISTS finance_tst.external_account_id CASCADE;

\echo '== [2/4] Dropping existing sequences =='

DROP SEQUENCE IF EXISTS finance_tst.vendors_vendor_number_seq                 CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.external_accounts_external_account_id_seq CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.payment_type_payment_type_id_seq          CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.voucher_type_type_code_seq                CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.company_id_seq                            CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.voucher_voucher_number_seq                CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.voucher_detail_id_seq                     CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.accounts_payable_id_seq                   CASCADE;
DROP SEQUENCE IF EXISTS finance_tst.asset_transfer_id_seq                     CASCADE;

\echo '== [3/4] Creating sequences =='

CREATE SEQUENCE finance_tst.vendors_vendor_number_seq                 START 1;
CREATE SEQUENCE finance_tst.external_accounts_external_account_id_seq START 1;
CREATE SEQUENCE finance_tst.payment_type_payment_type_id_seq          START 1;
CREATE SEQUENCE finance_tst.voucher_type_type_code_seq                START 1;
CREATE SEQUENCE finance_tst.company_id_seq                            START 1;
CREATE SEQUENCE finance_tst.voucher_voucher_number_seq                START 1;
CREATE SEQUENCE finance_tst.voucher_detail_id_seq                     START 1;
CREATE SEQUENCE finance_tst.accounts_payable_id_seq                   START 1;
CREATE SEQUENCE finance_tst.asset_transfer_id_seq                     START 1;

\echo '== [4/4] Creating tables =='

-- ----------------------------------------------------------------------------
-- Lookups (no FK dependencies within this set)
-- ----------------------------------------------------------------------------

CREATE TABLE finance_tst.company (
    id             integer          NOT NULL DEFAULT nextval('finance_tst.company_id_seq'),
    company_number integer          NOT NULL,
    company_name   character varying NOT NULL,
    CONSTRAINT company_pkey PRIMARY KEY (id)
);

CREATE TABLE finance_tst.payment_type (
    payment_type_id   integer               NOT NULL DEFAULT nextval('finance_tst.payment_type_payment_type_id_seq'),
    payment_type_text character varying(20) NOT NULL,
    CONSTRAINT payment_type_pkey PRIMARY KEY (payment_type_id)
);

CREATE TABLE finance_tst.voucher_type (
    type_code integer               NOT NULL DEFAULT nextval('finance_tst.voucher_type_type_code_seq'),
    type_text character varying(25) NOT NULL,
    CONSTRAINT voucher_type_pkey PRIMARY KEY (type_code)
);

CREATE TABLE finance_tst.vendors (
    vendor_number     integer               NOT NULL DEFAULT nextval('finance_tst.vendors_vendor_number_seq'),
    vendor_short_desc character varying(30) NOT NULL,
    vendor_address    character varying(60),
    CONSTRAINT vendors_pkey PRIMARY KEY (vendor_number)
);

CREATE TABLE finance_tst.external_accounts (
    external_account_id integer                NOT NULL DEFAULT nextval('finance_tst.external_accounts_external_account_id_seq'),
    account_name        character varying(100) NOT NULL,
    account_number      character varying(30)  NOT NULL,
    qualified           character varying(1),
    account_type        character varying(10),
    active              boolean                DEFAULT true,
    CONSTRAINT external_accounts_pkey PRIMARY KEY (external_account_id)
);

-- ----------------------------------------------------------------------------
-- Transactions (FK to lookups above)
-- ----------------------------------------------------------------------------

CREATE TABLE finance_tst.voucher (
    voucher_number    integer                  NOT NULL DEFAULT nextval('finance_tst.voucher_voucher_number_seq'),
    voucher_date      timestamp with time zone NOT NULL,
    voucher_ref       character varying(50),
    voucher_amt       numeric(10,2)            NOT NULL,
    voucher_type_id   integer,
    vendor_number     integer,
    payment_type_id   integer,
    payment_ref       character varying(50),
    payment_source_id integer,
    company_id        integer                  NOT NULL,
    CONSTRAINT voucher_pkey PRIMARY KEY (voucher_number),
    CONSTRAINT voucher_company_id_fkey          FOREIGN KEY (company_id)
        REFERENCES finance_tst.company(id),
    CONSTRAINT voucher_payment_source_id_fkey   FOREIGN KEY (payment_source_id)
        REFERENCES finance_tst.external_accounts(external_account_id),
    CONSTRAINT voucher_payment_type_id_fkey     FOREIGN KEY (payment_type_id)
        REFERENCES finance_tst.payment_type(payment_type_id),
    CONSTRAINT voucher_vendor_number_fkey       FOREIGN KEY (vendor_number)
        REFERENCES finance_tst.vendors(vendor_number),
    CONSTRAINT voucher_voucher_type_id_fkey     FOREIGN KEY (voucher_type_id)
        REFERENCES finance_tst.voucher_type(type_code)
);

CREATE TABLE finance_tst.voucher_detail (
    id               integer               NOT NULL DEFAULT nextval('finance_tst.voucher_detail_id_seq'),
    voucher_number   integer,
    split_seq_number integer               NOT NULL,
    account_number   character varying(10) NOT NULL,
    amount           numeric(10,2)         NOT NULL,
    dimension_1      character varying(20),
    dimension_2      character varying,
    memo             text,
    CONSTRAINT voucher_detail_pkey PRIMARY KEY (id),
    CONSTRAINT voucher_detail_voucher_number_fkey FOREIGN KEY (voucher_number)
        REFERENCES finance_tst.voucher(voucher_number)
);

CREATE TABLE finance_tst.accounts_payable (
    id                 integer                      NOT NULL DEFAULT nextval('finance_tst.accounts_payable_id_seq'),
    vendor_number      integer,
    stmt_dt            timestamp without time zone  NOT NULL,
    stmt_amt           double precision             NOT NULL,
    payment_due_dt     timestamp without time zone  NOT NULL,
    payment_source_id  integer,
    payment_voucher_id integer,
    invoice_id         character varying(25),
    vendor_account     integer,
    CONSTRAINT accounts_payable_pkey PRIMARY KEY (id),
    CONSTRAINT accounts_payable_payment_source_id_fkey  FOREIGN KEY (payment_source_id)
        REFERENCES finance_tst.external_accounts(external_account_id),
    CONSTRAINT accounts_payable_payment_voucher_id_fkey FOREIGN KEY (payment_voucher_id)
        REFERENCES finance_tst.voucher(voucher_number),
    CONSTRAINT accounts_payable_vendor_number_fkey      FOREIGN KEY (vendor_number)
        REFERENCES finance_tst.vendors(vendor_number),
    CONSTRAINT accounts_payable_vendor_account_fkey     FOREIGN KEY (vendor_account)
        REFERENCES finance_tst.external_accounts(external_account_id)
);

CREATE TABLE finance_tst.asset_transfer (
    id                      integer                  NOT NULL DEFAULT nextval('finance_tst.asset_transfer_id_seq'),
    transfer_date           timestamp with time zone NOT NULL,
    transfer_amount         numeric(10,2)            NOT NULL,
    src_external_account_id integer,
    tgt_external_account_id integer,
    memo                    text,
    CONSTRAINT asset_transfer_pkey PRIMARY KEY (id),
    CONSTRAINT asset_transfer_src_external_account_id_fkey FOREIGN KEY (src_external_account_id)
        REFERENCES finance_tst.external_accounts(external_account_id),
    CONSTRAINT asset_transfer_tgt_external_account_id_fkey FOREIGN KEY (tgt_external_account_id)
        REFERENCES finance_tst.external_accounts(external_account_id)
);

\echo '== finance_tst schema recreation complete =='
