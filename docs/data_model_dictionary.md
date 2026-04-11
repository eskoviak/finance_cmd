# Data Model and Dictionary: MyFinance Application

## Revision History

| Date | Change |
| -- | -- |
| 2026-03-10 | Original -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |
| 2026-03-14 | Added Register map Excel --> finance.register -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |
| 2026-03-31 | Updated and condensed in model notes -- [Ed Skoviak](smtp://eskoviak@eskoviak.com) |

## Data Entities

| Data Store | Collection  |
| --- | --- |
| [PostgreSQL](out/MyFinance-data-class/myfinance-data-class.png) | `finance` |
---

## Register Conversion

Create a mapping routine to read the data From Excel (`/Users/edmundlskoviak/iCloud/Documents/Excel/Banking.xlsx`) to insert into the finance.register table.  There are currently two tables to be converted:

1. CapOneRegister
2. Sch_010_Register

The following will not be transfered:

1. AMEX HYSA or Rewards Checking.  These have been (Rewards Checking) or will be closed (HYSA).
2. Amerirpise will be closed by end of march.

| Excel Column Name | Transformatiom | finance.application | Notes |
|--|--|--|--|
| -- | -- |id : sequence not null| no mapping, handled by engine during insert |
| Account | ??? |external_account_id : integer||
| Code | -- |code : integer||
| Date | Excel Date to ... |date : timestamp with time zone not null| |
| Description | -- |description : varchar(100)||
| Debit(-) | -- |debit : numeric(10,2)||
| IsFee | -- | isFee : boolean||
| Credit(-) | -- |credit : numeric(10,2)||
| Transnum | -- |tran_no : integer||
| Reconciled | -- |reconciled : boolean||
| Voucher | -- |voucher : integer||

*** Notes on finance.register.voucher

This field represents the id of the transaction details, which points to different table depending on the value of code.

| code | name | id points to table |
|--|--|--|
| 1 | Check | voucher  |   
| 2 | Debit Card | voucher  |
| 3 | Teller w/d | voucher  |
| 4 |ACH Payment | voucher  |
| 5 | Transfer | asset_transfer  |
| 6 | Interest | ???  |
| 7 | Direct Deposit | asset_transfer  |
| 8 | ATM Withdrawl | voucher  |
| 10 | ATM Fee | voucher, isFee = T  |
| 11 | Adjustment | ???
| 12 | Brokerage | voucher, transnum = Symbol  |
| 13 | Equities Dividend | asset_transfer ???  |
| 14 | Electronic Deposit | asset_transfer  |
| 15 | Maintenance Fees | voucher  |
| 16 | IRA Payout | asset_transfer  |
| 17 | Advisor Fee | ??? is this 15 |

The following will be used to update external_accounts.account_type

| Code | Meaning and Usage |
| -- | --- |
| CH | Checking |
| DB | Debit account |
| BRK | Brokerage  Account |
| SAV | Savings Account |
| CC | Credit Card |
| LN | Loan |
| HSA  | Health Savings Account |
| IRA | Individual Retirement Account |
| INV | Investment Account (institutional ) |

Currently, external_accounts also has revenue accounts (interest income, W2 Income, Pension Income, Other Revenue, etc.). Cleanup is necessary on this table as well, notably real account numbers (perhaps table need to be encrypted?)  Probably need to add Active column (This was completed with Issue 30).

## Data Cleanup `external_accounts` (Issue 42)

There are a number of records (196) assigend to external_account_id 19970 (Capital One Debit). These also have a a payment_type_id of 10 (debit).  These should be 10207 (which is what appears on receipts).  There are also a few assigned to external_acocunt_id 17542, which is the base checking account.  They need to also be moved to 10207.  To correct:
1. Add a new external_account_id for Capital One Debit (10207) at 
2. Move all records with (external_account_id = 19970 AND payment_type_id = 10) to 10207
3. Check that all records moved from 19970
4. Repeat for external_account_id = 17542 and payment_type_id = 10.
5. Check that all records moved from 17542
6. Removed entry 19970 from external_accounts table.

There are records of which match both cases in finance_tst.  Develop the scripts there and test.
